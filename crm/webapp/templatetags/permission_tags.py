from django import template
from webapp.models import PermissionGrant

register = template.Library()

@register.filter
def has_permission(user, permission):
    """Check if the logged-in user has been granted a specific permission"""
    try:
        if user.user_role.role == 'owner':
            return True
    except:
        return False
    return PermissionGrant.objects.filter(granted_to=user, permission=permission).exists()