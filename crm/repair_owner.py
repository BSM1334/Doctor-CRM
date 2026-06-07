import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth.models import User
from webapp.models import UserRole

def repair_owner():
    # Find the owner user (usually named 'owner' or is a superuser)
    owner = User.objects.filter(username='owner').first()
    if not owner:
        owner = User.objects.filter(is_superuser=True).first()
    
    if owner:
        role, created = UserRole.objects.get_or_create(user=owner)
        role.role = 'owner'
        role.is_approved = True
        if not role.phone:
            role.phone = '0000000000' # Dummy phone for owner if missing
        role.save()
        print(f"Success: User '{owner.username}' is now set as Owner and approved.")
    else:
        print("Error: No owner or superuser found. Please create one with 'python manage.py createsuperuser'.")

if __name__ == '__main__':
    repair_owner()
