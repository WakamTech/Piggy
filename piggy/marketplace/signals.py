# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import messaging

import firebase_admin
from firebase_admin import credentials, auth
import os




@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        # Notification pour l'utilisateur qui a passé la commande
        Notification.objects.create(
            user=instance.user,
            title='Commande validée',
            message=f'Votre commande {instance.id} a été validée avec succès',
        )
        # Notification pour le vendeur
        ad_seller = instance.ad.user  # Assumons que l'annonce a un champ 'user' qui fait référence au vendeur
        Notification.objects.create(
            user=ad_seller,
            title='Nouvelle commande',
            message=f'Commande {instance.id} validée avec succès par {instance.user.username}',
        )
        # Envoi de notifications FCM
        buyer = instance.user
        seller = instance.ad.user

