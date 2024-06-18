from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from geopy.distance import geodesic

from .models import User, Ad, Location, DeliveryFee, Butchery, Order, Notification, Review, Cart, OTP
from .serializers import UserSerializer, AdSerializer, LocationSerializer, DeliveryFeeSerializer, ButcherySerializer, OrderSerializer, NotificationSerializer, ReviewSerializer, CartSerializer, OTPSerializer

TWILIO_ACCOUNT_SID = 'votre_account_sid'
TWILIO_AUTH_TOKEN = 'votre_auth_token'
TWILIO_PHONE_NUMBER = 'votre_twilio_phone_number'

def geocode_address(address):
    geolocator = Nominatim(user_agent="piggy_geocoder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None

@api_view(['POST'])
def send_otp(request):
    phone = request.data.get('phone')
    if not phone:
        return Response({"error": "Numéro de téléphone requis."}, status=status.HTTP_400_BAD_REQUEST)

    code = OTP.generate_code()
    OTP.objects.create(phone=phone, code=code)
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f'Votre code OTP est {code}',
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )

    return Response({"message": "Code OTP envoyé."})

@api_view(['POST'])
def verify_otp(request):
    phone = request.data.get('phone')
    code = request.data.get('code')
    otp = OTP.objects.filter(phone=phone, code=code).first()

    if otp and otp.is_valid():
        otp.delete()
        return Response({"message": "Code OTP vérifié avec succès."})
    return Response({"error": "Code OTP invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    role = request.data.get('role', 'buyer')
    code = request.data.get('code')

    otp = OTP.objects.filter(phone=phone, code=code).first()
    if not otp or not otp.is_valid():
        return Response({"error": "Code OTP invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(phone=phone).exists():
        return Response({"error": "Numéro de téléphone déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(phone=phone, password=password, role=role)
    otp.delete()
    return Response({"message": "Inscription réussie.", "user_id": user.id})

@api_view(['POST'])
def login(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    user = authenticate(phone=phone, password=password)
    if user is not None:
        token = AccessToken.for_user(user)
        return Response({"token": str(token)})
    return Response({"error": "Informations d'identification incorrectes."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({"message": "Déconnexion réussie."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ad(request):
    serializer = AdSerializer(data=request.data)
    if serializer.is_valid():
        ad = serializer.save(user=request.user)
        address = request.data.get('address')
        if address:
            latitude, longitude = geocode_address(address)
            if latitude and longitude:
                Location.objects.create(ad=ad, latitude=latitude, longitude=longitude, address=address)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_ads(request):
    ads = Ad.objects.all()
    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_delivery_fee(request):
    user_location = Location.objects.get(user=request.user)
    destination_latitude = request.data.get('destination_latitude')
    destination_longitude = request.data.get('destination_longitude')
    
    if not destination_latitude or not destination_longitude:
        return Response({"error": "Destination coordinates are required"}, status=status.HTTP_400_BAD_REQUEST)

    user_coords = (user_location.latitude, user_location.longitude)
    destination_coords = (float(destination_latitude), float(destination_longitude))
    distance_km = geodesic(user_coords, destination_coords).kilometers
    
    delivery_fee = DeliveryFee.objects.first()
    total_fee = delivery_fee.base_fee + (distance_km * delivery_fee.fee_per_km)
    
    return Response({"total_fee": total_fee})
