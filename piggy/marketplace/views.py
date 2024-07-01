from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import AccessToken
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.contrib.auth import authenticate
from twilio.rest import Client
from django.core.exceptions import ObjectDoesNotExist
from .models import Config
from .models import User, Ad, Location, DeliveryFee, Butchery, Order, Notification, Review, Cart, OTP
from .serializers import UserSerializer, AdSerializer, LocationSerializer, DeliveryFeeSerializer, ButcherySerializer, OrderSerializer, NotificationSerializer, ReviewSerializer, CartSerializer, OTPSerializer
from django.db import models 
import logging

logger = logging.getLogger(__name__)

from .serializers import ConfigSerializer


import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_configs(request):
    keys = ['google_analytics_id', 'cloudinary_cloud_name', 'cloudinary_api_key', 'cloudinary_api_secret']
    configs = Config.objects.filter(key__in=keys)
    serializer = ConfigSerializer(configs, many=True)
    return Response(serializer.data)


def geocode_address(address):
    geolocator = Nominatim(user_agent="piggy_geocoder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None

@api_view(['POST'])
@permission_classes([])  # Cette ligne permet l'accès sans authentification
def send_otp(request):
    phone = request.data.get('phone')
    if not phone:
        return Response({"error": "Numéro de téléphone requis."}, status=status.HTTP_400_BAD_REQUEST)

    code = OTP.generate_code()
    print(code)
    OTP.objects.create(phone=phone, code=code)
    
    #client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    #try:
        #client.messages.create(
            #body=f'Votre code OTP est {code}',
            #from_=TWILIO_PHONE_NUMBER,
            #to=phone
        #)
    #except Exception as e:
        #return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Code OTP envoyé."})

@api_view(['POST'])
@permission_classes([])  # Cette ligne permet l'accès sans authentification
def verify_otp(request):
    phone = request.data.get('phone')
    code = request.data.get('code')
    otp = OTP.objects.filter(phone=phone, code=code).first()

    if otp and otp.is_valid():
        otp.delete()
        return Response({"message": "Code OTP vérifié avec succès."})
    return Response({"error": "Code OTP invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])  # Cette ligne permet l'accès sans authentification
def register(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    role = request.data.get('role', 'buyer')
    code = request.data.get('code')

    print(phone)
    print(code)

    otp = OTP.objects.filter(phone=phone, code=code).first()
    if not otp or not otp.is_valid():
        return Response({"error": "Code OTP invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(phone=phone).exists():
        return Response({"error": "Numéro de téléphone déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(phone=phone, password=password, role=role)
    otp.delete()
    user_serializer = UserSerializer(user)
    print(user_serializer.data)
    return Response({"message": "Inscription réussie.", "user": user_serializer.data})


@api_view(['POST'])
@permission_classes([])  # Cette ligne permet l'accès sans authentification
def login(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    print(f"Phone: {phone}, Password: {password}")  # Debug: Affiche les informations d'identification reçues
    user = authenticate(request, username=phone, password=password)  # Utilise `username` ici
    if user is not None:
        token = AccessToken.for_user(user)
        print(f"Login successful for user: {user}")  # Debug: Affiche un message de succès
        return Response({"token": str(token)})
    print("Authentication failed")  # Debug: Affiche un message d'échec
    return Response({"error": "Informations d'identification incorrectes."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({"message": "Déconnexion réussie."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    user_id = request.user.id
    return Response({"user_id": user_id})


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAdsListView(generics.ListAPIView):
    serializer_class = AdSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Ad.objects.filter(user__id=user_id)

class UserOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user__id=user_id)

class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        address = self.request.data.get('address')
        if address:
            latitude, longitude = geocode_address(address)
            if latitude and longitude:
                Location.objects.create(ad=serializer.instance, latitude=latitude, longitude=longitude, address=address)

class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        print("called")
        logger.debug("Delete method called")
        response = super().delete(request, *args, **kwargs)
        logger.debug("Delete operation completed with status %s", response.status_code)
        return response
    
    def perform_destroy(self, instance):
        instance.delete()

class DeliveryFeeListCreateView(generics.ListCreateAPIView):
    queryset = DeliveryFee.objects.all()
    serializer_class = DeliveryFeeSerializer
    permission_classes = [IsAuthenticated]

class DeliveryFeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryFee.objects.all()
    serializer_class = DeliveryFeeSerializer
    permission_classes = [IsAuthenticated]

class ButcheryListCreateView(generics.ListCreateAPIView):
    queryset = Butchery.objects.all()
    serializer_class = ButcherySerializer
    permission_classes = [IsAuthenticated]

class ButcheryAdsListView(generics.ListAPIView):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(user__role='butcher')

class ButcheryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Butchery.objects.all()
    serializer_class = ButcherySerializer
    permission_classes = [IsAuthenticated]

class UserOrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Récupère les commandes de l'utilisateur authentifié uniquement
        user = self.request.user
        return Order.objects.filter(user=user)

class UserOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Récupère les commandes de l'utilisateur authentifié uniquement
        user = self.request.user
        return Order.objects.filter(user=user)

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class NotificationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class CartRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    ad_id = request.data.get('ad_id')
    quantity = request.data.get('quantity', 1)

    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return Response({"error": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)

    cart, created = Cart.objects.get_or_create(user=user)

    # Add item to cart
    cart.items.append({"ad_id": ad_id, "quantity": quantity})
    cart.save()

    return Response({"message": "Item added to cart"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_delivery_fee(request):
    try:
        user_location = Location.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return Response({"error": "User location not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    destination_latitude = request.data.get('destination_latitude')
    destination_longitude = request.data.get('destination_longitude')
    
    if not destination_latitude or not destination_longitude:
        return Response({"error": "Destination coordinates are required"}, status=status.HTTP_400_BAD_REQUEST)

    user_coords = (user_location.latitude, user_location.longitude)
    destination_coords = (float(destination_latitude), float(destination_longitude))
    distance_km = geodesic(user_coords, destination_coords).kilometers
    
    delivery_fee = DeliveryFee.objects.first()
    if not delivery_fee:
        return Response({"error": "Delivery fee not found"}, status=status.HTTP_400_BAD_REQUEST)

    total_fee = delivery_fee.base_fee + (distance_km * delivery_fee.fee_per_km)
    
    return Response({"total_fee": total_fee})


from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Ad, Order
from .serializers import UserSerializer, AdSerializer, OrderSerializer

# Permission classes to restrict access to admin users only
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

# User Management
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        role = self.request.query_params.get('role', None)
        if role:
            return self.queryset.filter(role=role)
        return self.queryset

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # L'autorisation est accordée à l'admin ou si l'utilisateur est le propriétaire de l'objet.
        return obj == request.user or request.user.role == 'admin'

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

# Ad Management
class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status:
            return self.queryset.filter(is_active=(status == 'active'))
        return self.queryset

class AdValidateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk, format=None):
        try:
            ad = Ad.objects.get(pk=pk)
            ad.is_active = True
            ad.save()
            return Response({"message": "Annonce validée avec succès."}, status=status.HTTP_200_OK)
        except Ad.DoesNotExist:
            return Response({"error": "Annonce non trouvée."}, status=status.HTTP_404_NOT_FOUND)

class AdDeleteView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    permission_classes = [IsAdminUser]

# Order Management
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        if status:
            return self.queryset.filter(status=status)
        return self.queryset

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, F

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_stats(request):
    total_users = User.objects.count()
    total_ads = Ad.objects.count()
    total_orders = Order.objects.count()

    # Calculate the total revenue based on delivered orders
    revenue = Order.objects.filter(status='delivered').aggregate(
        total_revenue=Sum(F('quantity') * F('ad__price_per_kg'))
    )['total_revenue']

    return Response({
        "total_users": total_users,
        "total_ads": total_ads,
        "total_orders": total_orders,
        "revenue": revenue or 0
    })
