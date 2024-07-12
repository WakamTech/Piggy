from rest_framework import serializers
from .models import User, Ad, Location, DeliveryFee, Butchery, Order, Notification, Review, Cart, OTP
from rest_framework import generics
from rest_framework import serializers
from .models import Config

from rest_framework.renderers import JSONRenderer

class UTF8JSONRenderer(JSONRenderer):
    charset = 'utf-8'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('user',)  # Rend le champ 'user' en lecture seule

        extra_kwargs = {
            'city': {'required': False},
            'quantity': {'required': False},
            'price_per_kg': {'required': False},
            'weight_avg': {'required': False}
        }

    def create(self, validated_data):
        # Ajoutez la logique ici si nécessaire pour manipuler des données lors de la création
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fcm_token']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DeliveryFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFee
        fields = '__all__'

class ButcherySerializer(serializers.ModelSerializer):
    class Meta:
        model = Butchery
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['key', 'value']

class PriceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRule
        fields = '__all__' # Ou spécifiez les champs à exposer