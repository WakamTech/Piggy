from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials, auth
import os

# Initialiser Firebase Admin SDK
#cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'path_to_your_firebase_credentials.json'))
#firebase_admin.initialize_app(cred)

@receiver(post_save, sender=Order)
def handle_order_notification(sender, instance, created, **kwargs):
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
        #send_fcm_notification(instance.user, 'Commande validée', f'Votre commande {instance.id} a été validée avec succès')
        #send_fcm_notification(ad_seller, 'Nouvelle commande', f'Commande {instance.id} validée avec succès par {instance.user.username}')
    
    elif instance.status == 'cancelled':
        # Notification pour l'utilisateur qui a annulé la commande
        Notification.objects.create(
            user=instance.user,
            title='Commande annulée',
            message=f'Votre commande {instance.id} a été annulée',
        )
        # Notification pour le vendeur
        ad_seller = instance.ad.user  # Assumons que l'annonce a un champ 'user' qui fait référence au vendeur
        Notification.objects.create(
            user=ad_seller,
            title='Commande annulée',
            message=f'Commande {instance.id} a été annulée par {instance.user.username}',
        )
        # Envoi de notifications FCM
        #send_fcm_notification(instance.user, 'Commande annulée', f'Votre commande {instance.id} a été annulée')
        #send_fcm_notification(ad_seller, 'Commande annulée', f'Commande {instance.id} a été annulée par {instance.user.username}')

def send_fcm_notification(user, title, message):
    if user.profile.fcm_token:  # Assumons que le modèle UserProfile contient le token FCM
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=message,
            ),
            token=user.profile.fcm_token,
        )
        response = messaging.send(message)
        print('Successfully sent message:', response)
