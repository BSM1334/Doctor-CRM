from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# ============ USER ROLES ============

class UserRole(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('team_leader', 'Team Leader'),
        ('sales', 'Sales'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    team_number = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales')
    is_approved = models.BooleanField(default=False)  # For approval workflow
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    class Meta:
        ordering = ['-created_at']


# ============ SALES & TEAM LEADER MAPPING ============

class SalesTeamMapping(models.Model):
    """Maps sales to their team leader"""
    sales = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team_leader_mapping')
    team_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_members')
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        team_leader_name = self.team_leader.username if self.team_leader else "Unassigned"
        return f"{self.sales.username} -> {team_leader_name}"


# ============ CUSTOMER/CLIENT MODEL ============

class Customer(models.Model):
    STAGE_CHOICES = (
        ('phone_call', _('Phone Call')),
        ('personal_interview', _('Personal Interview')),
        ('location_visit', _('Location Visit')),
        ('contract_signed', _('Contract Signed')),
    )
    
    TYPE_CHOICES = (
        ('standard', _('Standard')),
        ('special', _('Special')),
    )
 
    # Basic Info
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers', verbose_name=_('Sales Rep'))
    first_name = models.CharField(max_length=250, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=250, verbose_name=_('Last Name'))
    phone = models.CharField(max_length=20, unique=True, verbose_name=_('Phone'))
    request = models.TextField(blank=True, verbose_name=_('Request'))
    customer_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='standard', verbose_name=_('Customer Type'))
 
    # Stage Tracking
    current_stage = models.CharField(max_length=30, choices=STAGE_CHOICES, default='phone_call', verbose_name=_('Current Stage'))
    stage_start_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Stage Start Date'))
 
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
 
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
 
    def is_in_danger_zone(self):
        """Check if customer is overdue for current stage (2 weeks)"""
        deadline = self.stage_start_date + timedelta(days=14)
        return timezone.now() > deadline and self.current_stage != 'contract_signed'
 
    def days_in_current_stage(self):
        """Get number of days in current stage"""
        delta = timezone.now() - self.stage_start_date
        return delta.days
 
    def whatsapp_link(self):
        """Generate WhatsApp link"""
        clean_phone = ''.join(filter(str.isdigit, self.phone))
        return f"https://wa.me/{clean_phone}"
 
    class Meta:
        ordering = ['-created_at']
        unique_together = ('sales_rep', 'phone')
        verbose_name = _('Customer')



# ============ CUSTOMER STAGE HISTORY ============

class CustomerStageHistory(models.Model):
    """Track stage changes for audit trail"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='stage_history')
    previous_stage = models.CharField(max_length=30, choices=Customer.STAGE_CHOICES)
    new_stage = models.CharField(max_length=30, choices=Customer.STAGE_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.first_name} - {self.previous_stage} -> {self.new_stage}"
    
    class Meta:
        ordering = ['-changed_at']


# ============ MONTHLY STATISTICS ============

class MonthlySalesStatistics(models.Model):
    """Track monthly customer acquisitions per sales rep"""
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_stats')
    year = models.IntegerField()
    month = models.IntegerField()  # 1-12
    customers_acquired = models.IntegerField(default=0)
    contracts_signed = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('sales_rep', 'year', 'month')
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.sales_rep.username} - {self.year}-{self.month:02d}: {self.customers_acquired} customers"


# ============ PERMISSION GRANTS ============

class PermissionGrant(models.Model):
    PERMISSION_CHOICES = [
        ('edit', 'Edit'),
        ('reset_password', 'Reset Password'),
        ('delete', 'Delete'),
    ]
    granted_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='granted_permissions')
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ('granted_to', 'permission')

    def __str__(self):
        return f"{self.granted_to.username} - {self.permission}"