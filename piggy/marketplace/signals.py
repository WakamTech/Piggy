from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials 
import os

# Initialiser Firebase Admin SDK
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

if GOOGLE_APPLICATION_CREDENTIALS:
    try:
        cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
        firebase_admin.initialize_app(cred)
    except ValueError as e:
        print(f"Erreur lors de l'initialisation de Firebase: {e}")
else:
    print("La variable d'environnement 'GOOGLE_APPLICATION_CREDENTIALS' n'est pas définie.")

@receiver(post_save, sender=Order)
def handle_order_notification(sender, instance, created, **kwargs):
    if created:
        # Notification pour l'utilisateur qui a passé la commande
        Notification.objects.create(
            user=instance.user,
            title='Commande validée',
            message=f'Votre commande {instance.id} a été validée avec succès',
        )
        send_fcm_notification(instance.user, 'Commande validée', f'Votre commande {instance.id} a été validée avec succès') 

        # Notification pour le vendeur
        ad_seller = instance.ad.user  
        Notification.objects.create(
            user=ad_seller,
            title='Nouvelle commande',
            message=f'Commande {instance.id} validée avec succès par {instance.user.username}',
        )
        send_fcm_notification(ad_seller, 'Nouvelle commande', f'Commande {instance.id} validée avec succès par {instance.user.username}')
    
    elif instance.status == 'cancelled':
        # Notification pour l'utilisateur qui a annulé la commande
        Notification.objects.create(
            user=instance.user,
            title='Commande annulée',
            message=f'Votre commande {instance.id} a été annulée',
        )
        send_fcm_notification(instance.user, 'Commande annulée', f'Votre commande {instance.id} a été annulée')

        # Notification pour le vendeur
        ad_seller = instance.ad.user
        Notification.objects.create(
            user=ad_seller,
            title='Commande annulée',
            message=f'Commande {instance.id} a été annulée par {instance.user.username}',
        )
        send_fcm_notification(ad_seller, 'Commande annulée', f'Commande {instance.id} a été annulée par {instance.user.username}')

def send_fcm_notification(user, title, message):
    if hasattr(user, 'profile') and user.profile.fcm_token:
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=user.profile.fcm_token,
            )
            response = messaging.send(message)
            print('Message envoyé avec succès :', response)
        except Exception as e:
            print(f"Erreur lors de l'envoi de la notification à {user.username}: {e}")