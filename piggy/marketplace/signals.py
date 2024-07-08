# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import messaging

import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ['FIREBASE_PROJECT_ID'],
    "private_key_id": os.environ['FIREBASE_PRIVATE_KEY_ID'],
    "private_key": os.environ['FIREBASE_PRIVATE_KEY'].replace('\\n', '\n'), # Important pour les clés multilignes
    "client_email": os.environ['FIREBASE_CLIENT_EMAIL'],
    "client_id": os.environ['FIREBASE_CLIENT_ID'],
    "auth_uri": os.environ['FIREBASE_AUTH_URI'],
    "token_uri": os.environ['FIREBASE_TOKEN_URI'],
    "auth_provider_x509_cert_url": os.environ['FIREBASE_AUTH_PROVIDER_X509_CERT_URL'],
    "client_x509_cert_url": os.environ['FIREBASE_CLIENT_X509_CERT_URL']
})

firebase_admin.initialize_app(cred)

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

        try:
            # Envoyer la notification FCM à l'acheteur
            if buyer.fcm_token:
                message = messaging.Message(
                    token=buyer.fcm_token,
                    notification=messaging.Notification(
                        title='Commande validée',
                        body=f'Votre commande {instance.id} a été validée avec succès'
                    )
                )
                response = messaging.send(message)
                print(f'Notification FCM envoyée à l\'acheteur (ID: {buyer.id}), message ID: {response}')
            else:
                print(f'L\'acheteur (ID: {buyer.id}) n\'a pas de jeton FCM enregistré.')

            # Envoyer la notification FCM au vendeur
            if seller.fcm_token:
                message = messaging.Message(
                    token=seller.fcm_token,
                    notification=messaging.Notification(
                        title='Nouvelle commande',
                        body=f'Commande {instance.id} validée par {buyer.username}'
                    )
                )
                response = messaging.send(message)
                print(f'Notification FCM envoyée au vendeur (ID: {seller.id}), message ID: {response}')
            else:
                print(f'Le vendeur (ID: {seller.id}) n\'a pas de jeton FCM enregistré.')
        except Exception as e:
            print(f'Erreur lors de l\'envoi des notifications FCM: {e}')