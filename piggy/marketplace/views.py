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
from django.contrib.admin.views.decorators import staff_member_required
logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model
from .serializers import ConfigSerializer
from rest_framework import generics
from .models import PriceRule
from .serializers import PriceRuleSerializer
from datetime import timedelta, date
from django.db.models import Count
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import FCMTokenSerializer 

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, F

import os
import firebase_admin
from firebase_admin import credentials, auth

from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
from .models import User, Ad, Order
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PriceRule
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import Ad
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Ad, Order
from .serializers import UserSerializer, AdSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ad
from geopy.geocoders import Nominatim
from geopy.distance import distance as geopy_distance
from rest_framework import generics
#... vos autres imports
from django.shortcuts import render
from .models import PromotionImage
from .serializers import PromotionImageSerializer # You'll need to make a Serializer if you haven't already! 
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.shortcuts import render
import cloudinary.uploader
from django.http import JsonResponse
from .models import PromotionImage  #  Ensure that you import PromotionImage
# ... (your existing views.py imports)

from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
# In your Django app's views.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from firebase_admin import messaging
from django.views.decorators.csrf import csrf_exempt
# ... other parts of views ... 

User = get_user_model()


class UTF8JSONRenderer(JSONRenderer):
    charset = 'utf-8'


def is_admin(user):
    return user.groups.filter(name='Administrateurs').exists()


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

    # Générer un code OTP à 6 chiffres
    code = str(random.randint(100000, 999999)) 
    print(code)

    try:
        # Envoyer le code OTP via Firebase
        # verification = auth.create_session_cookie(phone, {'code': code})
        #send_sms_verification_code(phone) #pour un SMS direct

        # Enregistrer le code OTP et le numéro de téléphone dans votre modèle OTP
        OTP.objects.create(phone=phone, code=code)
        
        return Response({"message": "Code OTP envoyé.", "verificationId": verification}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    full_name = request.data.get('full_name')
    role = request.data.get('role', 'buyer')
    #code = request.data.get('code')


    #otp = OTP.objects.filter(phone=phone, code=code).first()
    #if not otp or not otp.is_valid():
        #return Response({"error": "Code OTP invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(phone=phone).exists():
        return Response({"error": "Numéro de téléphone déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(phone=phone, password=password, role=role, full_name=full_name)
    #otp.delete()
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
    else : 
        print("Failed\nFailed")
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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):
    serializer = FCMTokenSerializer(instance=request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'FCM token saved successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    def put(self, request, *args, **kwargs):
        print("Données reçues:", request.data) # Affichez les données reçues
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("Données validées et enregistrées:", serializer.data)
            return Response(serializer.data)
        else:
            print("Erreurs de validation:", serializer.errors) # Affiche les erreurs de validation
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        price = self.request.data.get('price_per_kg')
        initial_price = price  # Enregistrer le prix initia
        role = self.request.data.get('type')

        try:
            # Chercher une règle spécifique pour le rôle donné
            rule = PriceRule.objects.get(role=role, min_price__lte=price) 
            
            # Si une règle existe, appliquer la logique de la règle
            if rule.fixed_price is not None:
                new_price = price + rule.fixed_price
            elif rule.price_increase_percentage is not None:
                increase_amount = price * (rule.price_increase_percentage / 100) 
                new_price = price + increase_amount 
            else:
                new_price = price  
        
        except PriceRule.DoesNotExist:
            # Gérer le cas où aucune règle n'est trouvée, appliquer une logique par défaut (spécifique au rôle)
            new_price = price
            if role == 'butcher':
                new_price = price + 200 
            elif role == 'buyer':  # Utiliser 'elif' pour une meilleure lisibilité
                new_price = price 
            elif role == 'farmer': 
                new_price = price + 200

        # Enregistrer l'annonce avec le prix ajusté
        serializer.save(user=self.request.user, price_per_kg=new_price, initial_price_per_kg=initial_price)

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
        print("\n\n\nnnn")
        return self.partial_update(request, *args, **kwargs)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_ad(request):
    ad_id = request.data.get('ad_id')

    if not ad_id:
        return Response({"error": "Missing ad_id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ad = Ad.objects.get(pk=ad_id)
        ad.delete()
        return Response({"message": "Ad deleted successfully."}, status=status.HTTP_200_OK)
    except Ad.DoesNotExist:
        return Response({"error": "Ad not found."}, status=status.HTTP_404_NOT_FOUND)
    

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_butchery_ads(request):
    ads = Ad.objects.filter(type='butcher')

    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)


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

class UserNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

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
def empty_cart(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
        cart.items.clear()  # Clear all items in the cart
        cart.save()
        return Response({"message": "Cart emptied successfully"}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

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




# Permission classes to restrict access to admin users only
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


User = get_user_model()

@api_view(['GET'])
@permission_classes([])  # Cette ligne permet l'accès sans authentification
def dashboard(request):
    
    # Statistiques des utilisateurs
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()

    # Statistiques des annonces
    total_ads = Ad.objects.count()
    active_ads = Ad.objects.filter(is_active=True).count()

    # Statistiques des commandes
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    delivered_orders = Order.objects.filter(status='delivered').count()

    # Statistiques des rôles des utilisateurs
    

     # Calculate the total revenue based on delivered orders
    revenue = Order.objects.filter(status='delivered').aggregate(
        total_revenue=Sum(F('quantity') * F('ad__price_per_kg'))
    )['total_revenue']

    
    # Préparation du contexte pour le template
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_ads': total_ads,
        'active_ads': active_ads,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'revenue' : revenue
        
    }    
    return render(request, 'marketplace/index.html', context)




# User Management
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role', None)
        if role:
            return queryset.filter(role=role)
        return queryset

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
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        if status == 'active':
            return queryset.filter(is_active=True)
        elif status == 'inactive':
            return queryset.filter(is_active=False)
        return queryset

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Commande non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if new_status not in [choice[0] for choice in Order.STATUS_CHOICES]:
        return Response({'error': 'Statut non valide.'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()
    return Response({'success': 'Statut de la commande mis à jour.'}, status=status.HTTP_200_OK) 
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
    permission_classes = [IsOwnerOrAdmin]

# Order Management
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get('status', None)
        if status:
            return queryset.filter(status=status)
        return queryset

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]



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

     # Calculate the current revenue based on 'accepted' orders 
    current_revenue  = 0 
    current_revenue = Order.objects.filter(status='accepted').aggregate(
        total_current_revenue=Sum(F('quantity') * F('ad__price_per_kg')) 
    )['total_current_revenue']

    manager_revenue = 0
    for order in Order.objects.filter(status__in=['accepted', 'pending', 'delivered']):
        price_difference = order.ad.price_per_kg - order.ad.initial_price_per_kg
        manager_revenue += price_difference * order.quantity

    roles = User.ROLE_CHOICES
    user_roles_count = {role[0]: User.objects.filter(role=role[0]).count() for role in roles}

    today = date.today()
    last_week_start = today - timedelta(days=30)

    orders_evolution = Ad.objects.filter(created_at__range=(last_week_start, today)).values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')

    print(list(orders_evolution) )
    return Response({
        "total_users": total_users,
        "total_ads": total_ads,
        "total_orders": total_orders,
        "current_revenue": current_revenue,   # new
        "manager_revenue" : manager_revenue,
        'user_roles': user_roles_count,
        'orders_evolution' : list(orders_evolution) 
    })

geolocator = Nominatim(user_agent="piggy_geocoder")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nearby_farmers_ads(request):
    ads = Ad.objects.filter(type='farmer')

    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nearby_buyers_ads(request):
    ads = Ad.objects.filter(type='buyer')
    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)
# ...

class PriceRuleListView(generics.ListCreateAPIView):
    queryset = PriceRule.objects.all()
    serializer_class = PriceRuleSerializer
    permission_classes = [IsAdminUser] 

    def create(self, request, *args, **kwargs):
            print("Données reçues dans la vue create():", request.data)
            return super().create(request, *args, **kwargs)


class PriceRuleDeleteView(generics.DestroyAPIView):
    queryset = PriceRule.objects.all()
    serializer_class = PriceRuleSerializer  # Optionnel, mais peut être utile pour la validation 
    permission_classes = [IsAdminUser] 





# Note, the use of  @permission_classes. If using JWTs, ensure you have JWT auth setup 
@api_view(['GET']) 
@permission_classes([IsAdminUser]) 
def get_promotion_images(request):
    promotion_images = PromotionImage.objects.all() # retrieve all images (check your database for foreign keys and filtering logic here).
    serializer = PromotionImageSerializer(promotion_images, many=True)  # Make sure to properly serializer to a response
    return Response(serializer.data)

@api_view(['POST']) 
@permission_classes([IsAdminUser])  # For authorization!  
def add_promotion_image_url(request):
  if request.method == 'POST': 
    new_url = request.data.get('url') # The data from the post

    if not new_url:
        return Response({'error': 'L’URL de l’image est requise.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
     # Ensure it's not more than 5 (you need the correct Django code logic for counting, it
      # will differ if you are storing them per User). If storing in a more general
      # context you can try to limit the number of URLs.  
        current_count = PromotionImage.objects.count() 
        if current_count >= 5: 
            return Response({'error': 'Limite de 5 images atteinte.'}, status=status.HTTP_400_BAD_REQUEST)

        new_image = PromotionImage.objects.create(user=user, url=new_url) 
        new_image.save() 

        serializer = PromotionImageSerializer(new_image) #  For a JSON response
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': f'Erreur lors de l\'ajout de l\'image: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['POST']) 
@permission_classes([])  # For authorization!  
def upload_promotion_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Extracting image data from the request.FILES dictionary
            image = request.FILES['image'] 

            # Optional resizing or other validation here before upload
            # You can resize the image, change format, crop it. etc.

            result = cloudinary.uploader.upload(
                image, 
                #folder="my_folder_for_promotion_images" # Optionally you could make a special cloudinary folder 
            )
            # Debugging:  print the result (or you can add logging for Django).
            print(result) 
            # Response sends URL and the message 'success'
            return JsonResponse({'success': True, 'url': result['secure_url']})

        except Exception as e:
            print(f"Error during image upload: {e}") # Debugging for your Django view
            # Sending a 'success': False, and error message. You can return the error message or custom message here. 
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Veuillez choisir un fichier.'}, status=400) 






 
  # Update View: For storing URLs.  
@api_view(['PATCH'])
@permission_classes([IsAdminUser]) # make sure to secure 
def update_cloudinary_config(request, format=None): 
    cloudinary_cloud_name = request.data.get('cloudinary_cloud_name') 
    cloudinary_api_key = request.data.get('cloudinary_api_key')
    cloudinary_api_secret = request.data.get('cloudinary_api_secret') 

    if not all([cloudinary_cloud_name, cloudinary_api_key, cloudinary_api_secret]):
            return Response({'error': 'All Cloudinary fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        #  You will likely have to handle authentication or user id  
        # if this is related to a User here - for example, your Django JWT
        # code (if you are using JWTs). You may need to pass the `User.objects.get` as well 
        # assuming you want to attach this to the current User
        user = request.user # or how to access your user is your logic

        
        # Create your models (if they don't already exist) 
        # config, created = Config.objects.update_or_create(
        #       key="cloudinary_cloud_name",
        #        defaults={'value': cloudinary_cloud_name} 
        #   ) 
        # config, created = Config.objects.update_or_create( 
        #       key='cloudinary_api_key', 
        #       defaults={'value': cloudinary_api_key} 
        #   )
        # config, created = Config.objects.update_or_create( 
        #       key='cloudinary_api_secret',
        #       defaults={'value': cloudinary_api_secret} 
        #   ) 
        # You might have to load settings to update here if they have already been initialized in a settings.py function!
        
        # Use the new values with Cloudinary.config
        cloudinary.config(
            cloud_name=cloudinary_cloud_name,  
            api_key=cloudinary_api_key,  
            api_secret=cloudinary_api_secret 
        ) 

        return Response({'message': 'Configuration mise à jour avec succès.'})
    except Exception as e:
        return Response({'error': f'Erreur lors de la mise à jour: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@csrf_exempt
def send_update_notification(request):
    if request.method == 'POST':
        try:
            # Fetch users or use a filter to target specific users
            users = User.objects.all()  # or use a specific queryset
            title = "Nouvelle mise à jour disponible"
            body = "Une nouvelle mise à jour disponible. Vérifiez sur le play store"

            for user in users:
                if hasattr(user, 'profile') and user.profile.fcm_token:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=title,
                            body=body,
                        ),
                        token=user.profile.fcm_token,
                    )
                    messaging.send(message)

            return JsonResponse({'status': 'success', 'message': 'Notifications sent successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
