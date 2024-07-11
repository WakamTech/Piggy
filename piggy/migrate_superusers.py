from marketplace.models import User  # Assurez-vous que le chemin d'accès est correct
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Convertit les superutilisateurs en utilisateurs admin"

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        for superuser in superusers:
            superuser.role = "admin"
            #superuser.is_superuser = False  # Facultatif : supprimez les privilèges de superutilisateur
            #superuser.is_staff = False # Facultatif : supprimez les privilèges de staff
            superuser.save()
            self.stdout.write(self.style.SUCCESS(f"Utilisateur '{superuser.phone}' converti en admin avec succès."))