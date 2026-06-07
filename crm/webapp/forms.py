from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import PasswordInput, TextInput, Select, Textarea
from .models import Customer, UserRole
from django.utils.translation import get_language

def get_phone_widget():
    lang = get_language()
    align = 'left' if lang == 'en' else 'right'
    return forms.TextInput(attrs={
        'class': 'form-control',
        'dir': 'ltr',
        'style': f'text-align: {align};',
    })

# ============ AUTHENTICATION FORMS ============

class RegisterForm(UserCreationForm):
    """Registration form with role selection"""
    ROLE_CHOICES = (
        ('sales', _('Sales Representative')),
        ('team_leader', _('Team Leader')),
    )

    phone = forms.CharField(
        label=_('Phone Number'),
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'phone': get_phone_widget(),
            'class': 'form-control'
        }),
        help_text=_('Format: + [Country Code] [Number]')
    )
    team_number = forms.CharField(
        label=_('Team Number'),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'phone': get_phone_widget(),
            'class': 'form-control'
        }),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(),
        required=True,
        help_text=_('Select your designation in the company')
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
            
        # Check both Users and Customers
        if UserRole.objects.filter(phone=phone).exists() or Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered in the system.")
        return phone

    def clean_team_number(self):
        team_number = self.cleaned_data.get('team_number')
        role = self.cleaned_data.get('role')
        if role == 'team_leader' and not team_number:
            raise forms.ValidationError(_('Team Number is required for Team Leaders.'))
        return team_number


class LoginForm(AuthenticationForm):
    """Login form"""
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control'
    }))
    phone = forms.CharField(
        label=_('Phone'),
        widget=TextInput(attrs={
            'phone': get_phone_widget(),
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=PasswordInput(attrs={
            'class': 'form-control'
        })
    )
class OwnerLoginForm(AuthenticationForm):
    """Owner login form (Name and Password only)"""
    username = forms.CharField(label=_('Name'), widget=TextInput(attrs={
        'class': 'form-control',
    }))
    password = forms.CharField(label=_('Password'),widget=PasswordInput(attrs={
        'class': 'form-control',
    }))


# ============ CUSTOMER FORMS ============

class CreateCustomerForm(forms.ModelForm):
    days_in_stage = forms.IntegerField(
        required=False,
        initial=0,
        label=_('Days in Stage'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
    )

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'sales_rep', 'request', 'current_stage', 'customer_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'sales_rep': forms.Select(attrs={'class': 'form-control'}),
            'request': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'current_stage': forms.Select(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone': _('Phone'),
            'request': _('Request'),
            'current_stage': _('Current Stage'),
            'sales_rep': _('Assigned Sales Rep'),
            'customer_type': _('Customer Type'),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # If sales rep, remove the sales_rep field (will be set to current user)
        if user and user.user_role.role == 'sales':
            self.fields.pop('sales_rep', None)
        else:
            # For team leaders, show only their team members plus themselves
            if user and user.user_role.role == 'team_leader':
                from django.db.models import Q
                team_members = User.objects.filter(
                    Q(team_leader_mapping__team_leader=user, user_role__role='sales', user_role__is_approved=True) |
                    Q(id=user.id),
                    user_role__is_approved=True
                ).select_related('user_role').distinct().order_by('username')
                self.fields['sales_rep'].queryset = team_members
                # Pre-select the team leader as the assigned sales rep
                self.fields['sales_rep'].initial = user.id
            else:
                # Default: show both sales and team_leader roles
                self.fields['sales_rep'].queryset = User.objects.filter(
                    user_role__role__in=['sales', 'team_leader'],
                    user_role__is_approved=True
                ).select_related('user_role').order_by('user_role__role', 'username')
            
            # Custom choices to display role with username
            choices = [('', '---------')]
            for user_obj in self.fields['sales_rep'].queryset:
                role_display = user_obj.user_role.get_role_display()
                choices.append((user_obj.id, f"{user_obj.username} ({role_display})"))
            self.fields['sales_rep'].choices = choices

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        if UserRole.objects.filter(phone=phone).exists() or Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered in the system.")
        return phone

class AdminCreateCustomerForm(forms.ModelForm):
    """Form for admins to create customers with stage and manual duration"""
    days_in_stage = forms.IntegerField(
        required=False,
        initial=0,
        label=_('Days in Stage'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        help_text=_('Number of days the customer has already been in this stage.')
    )
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'request', 'current_stage', 'customer_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                
            }),
            'request': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'current_stage': forms.Select(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone': _('Phone'),
            'request': _('Request'),
            'current_stage': _('Current Stage'),
            'customer_type': _('Customer Type'),
            'sales_rep': _('Sales'),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
            
        # Check both Users and Customers
        if UserRole.objects.filter(phone=phone).exists() or Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered in the system.")
        return phone

    def save(self, commit=True):
        instance = super().save(commit=False)
        days = self.cleaned_data.get('days_in_stage', 0) or 0
        if days > 0:
            from django.utils import timezone
            from datetime import timedelta
            instance.stage_start_date = timezone.now() - timedelta(days=days)
        if commit:
            instance.save()
        return instance


class UpdateCustomerForm(forms.ModelForm):
    """Form to update customer details including assignment and stage"""
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'sales_rep', 'current_stage', 'request']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                
            }),
            'sales_rep': forms.Select(attrs={'class': 'form-control'}),
            'current_stage': forms.Select(attrs={'class': 'form-control'}),
            'request': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone': _('Phone'),
            'request': _('Request'),
            'current_stage': _('Current Stage'),
            'sales_rep': _('Sales'),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
            
        # Check both Users (all) and Customers (excluding this one)
        if UserRole.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number belongs to a staff member.")
            
        customer_qs = Customer.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            customer_qs = customer_qs.exclude(pk=self.instance.pk)
            
        if customer_qs.exists():
            raise forms.ValidationError("This phone number is already assigned to another customer.")
            
        return phone


class UpdateCustomerStageForm(forms.ModelForm):
    """Form to update customer stage"""
    class Meta:
        model = Customer
        fields = ['current_stage']
        widgets = {
            'current_stage': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# ============ USER MANAGEMENT FORMS ============

class EditUserForm(forms.ModelForm):
    """Form to edit user details"""
    phone = forms.CharField(
        label=_('Phone Number'),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'phone': get_phone_widget(),
            'class': 'form-control'
        }),
        help_text=_('Format: + [Country Code] [Number]')
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            try:
                self.fields['phone'].initial = self.instance.user_role.phone
            except UserRole.DoesNotExist:
                pass

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        # Check Users (excluding this one)
        user_qs = UserRole.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            user_qs = user_qs.exclude(user=self.instance)
        
        if user_qs.exists():
            raise forms.ValidationError("This phone number is already registered to another user.")
            
        # Check Customers
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered to a customer.")
            
        return phone


class EditSalesRepForm(forms.ModelForm):
    """Specialized form for Sales Representatives (Name, Phone, Team Leader)"""
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'phone': get_phone_widget(),
            'class': 'form-control'
        }),
        label=_('Phone Number')
    )
    team_leader = forms.ModelChoiceField(
        queryset=User.objects.filter(user_role__role='team_leader'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Team Leader')
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': _('Name'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Initialize phone from UserRole
            try:
                self.fields['phone'].initial = self.instance.user_role.phone
            except UserRole.DoesNotExist:
                pass
            
            # Initialize team_leader from SalesTeamMapping
            try:
                mapping = self.instance.team_leader_mapping
                self.fields['team_leader'].initial = mapping.team_leader
            except:
                pass

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        # Check Users (excluding this one)
        user_qs = UserRole.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            user_qs = user_qs.exclude(user=self.instance)
        
        if user_qs.exists():
            raise forms.ValidationError("This phone number is already registered to another user.")
            
        # Check Customers
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered to a customer.")
            
        return phone


class EditTeamLeaderForm(forms.ModelForm):
    """Specialized form for Team Leaders (Name, Phone)"""
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'phone': get_phone_widget(),
            'class': 'form-control'
        }),
        label=_('Phone Number')
    )
    team_number = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label=_('Team Number')
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': _('Name'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Initialize phone from UserRole
            try:
                self.fields['phone'].initial = self.instance.user_role.phone
                self.fields['team_number'].initial = self.instance.user_role.team_number
            except UserRole.DoesNotExist:
                pass

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        # Check Users (excluding this one)
        user_qs = UserRole.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            user_qs = user_qs.exclude(user=self.instance)
        
        if user_qs.exists():
            raise forms.ValidationError("This phone number is already registered to another user.")
            
        # Check Customers
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered to a customer.")
            
        return phone
