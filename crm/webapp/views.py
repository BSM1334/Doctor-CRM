from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
import logging
import secrets
import string
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _

from .models import (
    UserRole, Customer, SalesTeamMapping, 
    CustomerStageHistory, MonthlySalesStatistics, PermissionGrant
)
from .forms import (
    RegisterForm, LoginForm, CreateCustomerForm, 
    UpdateCustomerForm, UpdateCustomerStageForm, OwnerLoginForm,
    AdminCreateCustomerForm
)

logger = logging.getLogger(__name__)


# ============ UTILITY FUNCTIONS ============

def get_user_role(user):
    try:
        return user.user_role.role
    except UserRole.DoesNotExist:
        return None


def is_owner(user):
    return get_user_role(user) == 'owner'


def is_team_leader(user):
    return get_user_role(user) == 'team_leader'


def is_sales(user):
    return get_user_role(user) == 'sales'


def get_user_team_leader(user):
    if is_sales(user):
        try:
            return user.team_leader_mapping.team_leader
        except:
            return None
    return None


def get_team_sales(user):
    if is_team_leader(user):
        return User.objects.filter(team_leader_mapping__team_leader=user)
    return User.objects.none()


def can_access_customer(user, customer):
    """Check if user can access a customer record"""
    return (
        customer.sales_rep == user or
        is_owner(user) or
        is_team_leader(user)
    )

def has_permission(user, permission):
    if is_owner(user):
        return True
    return PermissionGrant.objects.filter(granted_to=user, permission=permission).exists()


# ============ AUTHENTICATION VIEWS ============

def home(request):
    if request.user.is_authenticated:
        if is_owner(request.user):
            return redirect('owner_dashboard')
        elif is_team_leader(request.user):
            return redirect('team_leader_dashboard')
        else:
            return redirect('sales_dashboard')
    return render(request, 'webapp/index.html')


def register(request):
    if request.user.is_authenticated:
        if is_owner(request.user):
            return redirect('owner_dashboard')
        elif is_team_leader(request.user):
            return redirect('team_leader_dashboard')
        else:
            return redirect('sales_dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            role = form.cleaned_data.get('role')
            phone = form.cleaned_data.get('phone')
            team_number = form.cleaned_data.get('team_number') if role == 'team_leader' else None
            UserRole.objects.create(
                user=user,
                role=role,
                phone=phone,
                team_number=team_number,
                is_approved=False
            )
            messages.success(request, 'Account created! Please wait for owner approval.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegisterForm()
    
    return render(request, 'webapp/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if is_owner(request.user):
            return redirect('owner_dashboard')
        elif is_team_leader(request.user):
            return redirect('team_leader_dashboard')
        else:
            return redirect('sales_dashboard')
    
    if request.session.get('logout_message'):
        messages.error(request, 'You have logged out.')
        del request.session['logout_message']
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                if not user.user_role.is_approved:
                    messages.error(request, 'Your account is pending owner approval.')
                    return redirect('login')
            except UserRole.DoesNotExist:
                messages.error(request, 'User role not found. Please contact administrator.')
                return redirect('login')
            
            login(request, user)
            messages.success(request, f'Welcome {user.username}!')
            
            if is_owner(user):
                return redirect('owner_dashboard')
            elif is_team_leader(user):
                return redirect('team_leader_dashboard')
            else:
                return redirect('sales_dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'webapp/login.html', {'form': form})


def owner_login(request):
    if request.user.is_authenticated:
        if is_owner(request.user):
            return redirect('owner_dashboard')
        elif is_team_leader(request.user):
            return redirect('team_leader_dashboard')
        return redirect('sales_dashboard')
    
    if request.method == 'POST':
        form = OwnerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not is_owner(user):
                messages.error(request, 'This login is for the Owner only.')
                return redirect('owner_login')
            if not user.user_role.is_approved:
                messages.error(request, 'Owner account is not approved.')
                return redirect('owner_login')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('owner_dashboard')
        else:
            messages.error(request, 'Invalid name or password.')
    else:
        form = OwnerLoginForm()
    
    return render(request, 'webapp/owner_login.html', {'form': form})


def logout_view(request):
    logout(request)
    request.session['logout_message'] = True
    return redirect('login')


# ============ SALES DASHBOARD ============

@never_cache
@login_required(login_url='login')
def sales_dashboard(request):
    user_role = get_user_role(request.user)
    if user_role not in ['sales', 'team_leader']:
        return redirect('login')
    
    customers = Customer.objects.filter(sales_rep=request.user)
    total_customers = customers.count()
    contracts_signed = customers.filter(current_stage='contract_signed').count()
    in_progress = total_customers - contracts_signed
    danger_zone = sum(1 for c in customers if c.is_in_danger_zone())
    
    today = timezone.now()
    monthly_stats, created = MonthlySalesStatistics.objects.get_or_create(
        sales_rep=request.user,
        year=today.year,
        month=today.month
    )
    
    danger_customers = [c for c in customers if c.is_in_danger_zone()]
    
    context = {
        'total_customers': total_customers,
        'contracts_signed': contracts_signed,
        'in_progress': in_progress,
        'danger_zone': danger_zone,
        'monthly_acquisitions': monthly_stats.customers_acquired,
        'customers': customers,
        'danger_customers': danger_customers,
        'team_leader': get_user_team_leader(request.user),
    }
    
    return render(request, 'webapp/sales_dashboard.html', context)


@login_required(login_url='login')
def team_leader_dashboard(request):
    if not is_team_leader(request.user):
        messages.error(request, 'TEAM LEADER CHECK FAILED')
        return redirect('home')
    
    sales_reps = UserRole.objects.filter(
        user__team_leader_mapping__team_leader=request.user,
        role='sales',
        is_approved=True
    ).select_related('user')
    
    team_users = [sr.user for sr in sales_reps]
    team_users.append(request.user)
    total_team_customers = Customer.objects.filter(sales_rep__in=team_users).count()
    total_team_contracts = Customer.objects.filter(sales_rep__in=team_users, current_stage='contract_signed').count()
    own_customers = Customer.objects.filter(sales_rep=request.user).order_by('-created_at')
    
    team_number = None
    try:
        team_number = request.user.user_role.team_number
    except UserRole.DoesNotExist:
        pass

    context = {
        'sales_reps': sales_reps,
        'total_team_customers': total_team_customers,
        'total_team_contracts': total_team_contracts,
        'team_size': sales_reps.count(),
        'team_number': team_number,
        'own_customers': own_customers,
    }
    
    return render(request, 'webapp/team_leader_dashboard.html', context)


@login_required(login_url='login')
def create_customer(request):
    storage = messages.get_messages(request)
    storage.used = True 
    if not (is_sales(request.user) or is_team_leader(request.user)):
        return redirect('home')
    
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST, user=request.user)
        if form.is_valid():
            customer = form.save(commit=False)
            
            # If sales rep, set sales_rep to current user
            if is_sales(request.user):
                customer.sales_rep = request.user
            
            # Set stage start date based on days_in_stage
            days = int(request.POST.get('days_in_stage', 0))
            if days > 0:
                from datetime import timedelta
                customer.stage_start_date = timezone.now() - timedelta(days=days)
            customer.save()
            
            today = timezone.now()
            stats, created = MonthlySalesStatistics.objects.get_or_create(
                sales_rep=customer.sales_rep,
                year=today.year,
                month=today.month
            )
            stats.customers_acquired += 1
            stats.save()
            
            messages.success(request, 'Customer added successfully!')
            if is_team_leader(request.user):
                return redirect('team_leader_dashboard')
            return redirect('sales_dashboard')
        else:
            if 'phone' in form.errors:
                messages.error(request, 'This phone number is already registered.')
            else:
                messages.error(request, 'Failed to add customer. Please check the form.')
    else:
        form = CreateCustomerForm(user=request.user)
    
    dashboard_name = 'team_leader_dashboard' if is_team_leader(request.user) else 'sales_dashboard'
    return render(request, 'webapp/create_customer.html', {'form': form, 'dashboard_url_name': dashboard_name})


@login_required(login_url='login')
def view_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if not can_access_customer(request.user, customer):
        return redirect('sales_dashboard')
    
    history = list(customer.stage_history.all())
    for h in history:
        h.changed_at_fixed = h.changed_at + timedelta(hours=3)
        
    context = {
        'customer': customer,
        'whatsapp_link': customer.whatsapp_link(),
        'is_danger': customer.is_in_danger_zone(),
        'days_in_stage': customer.days_in_current_stage(),
        'created_at_fixed': customer.created_at + timedelta(hours=3),
        'updated_at_fixed': customer.updated_at + timedelta(hours=3),
        'stage_history': history,
        'from_sales_rep': request.GET.get('from_sales_rep'),
    }
    
    return render(request, 'webapp/view_customer.html', context)


@login_required(login_url='login')
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if not can_access_customer(request.user, customer) and not PermissionGrant.objects.filter(granted_to=request.user, permission='edit').exists():
        return redirect('sales_dashboard')
    
    if request.method == 'POST':
        old_stage = customer.current_stage
        form = UpdateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            new_customer = form.save(commit=False)
            if new_customer.current_stage != old_stage:
                new_customer.stage_start_date = timezone.now()
                new_customer.save()
                CustomerStageHistory.objects.create(
                    customer=new_customer,
                    previous_stage=old_stage,
                    new_stage=new_customer.current_stage
                )
                if new_customer.current_stage == 'contract_signed':
                    today = timezone.now()
                    stats, created = MonthlySalesStatistics.objects.get_or_create(
                        sales_rep=new_customer.sales_rep,
                        year=today.year,
                        month=today.month
                    )
                    stats.contracts_signed += 1
                    stats.save()
            else:
                new_customer.save()
                
            messages.success(request, 'Customer updated successfully!')
            return redirect('view_customer', customer_id=customer.id)
    else:
        form = UpdateCustomerForm(instance=customer)
    
    # Limit sales reps shown based on editor role
    if is_team_leader(request.user):
        # Show only this team leader and their approved sales members
        sales_reps = User.objects.filter(
            Q(team_leader_mapping__team_leader=request.user, user_role__role='sales', user_role__is_approved=True) |
            Q(id=request.user.id)
        ).select_related('user_role').distinct().order_by('username')
    else:
        # Default: show all approved sales and team leaders, but include current assigned rep
        sales_reps = User.objects.filter(
            Q(user_role__role__in=['sales', 'team_leader'], user_role__is_approved=True) | Q(id=customer.sales_rep.id)
        ).select_related('user_role').distinct().order_by('user_role__role', 'username')

    return render(request, 'webapp/update_customer.html', {'form': form, 'customer': customer, 'sales_reps': sales_reps})


@login_required(login_url='login')
def update_customer_stage(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if not can_access_customer(request.user, customer):
        return redirect('sales_dashboard')
    
    if request.method == 'POST':
        form = UpdateCustomerStageForm(request.POST, instance=customer)
        if form.is_valid():
            old_stage = customer.current_stage
            customer = form.save(commit=False)
            customer.stage_start_date = timezone.now()
            customer.save()
            
            CustomerStageHistory.objects.create(
                customer=customer,
                previous_stage=old_stage,
                new_stage=customer.current_stage
            )
            
            if customer.current_stage == 'contract_signed':
                today = timezone.now()
                stats, created = MonthlySalesStatistics.objects.get_or_create(
                    sales_rep=customer.sales_rep,
                    year=today.year,
                    month=today.month
                )
                stats.contracts_signed += 1
                stats.save()
            
            messages.success(request, f'Customer moved to {customer.get_current_stage_display()}!')
            return redirect('view_customer', customer_id=customer.id)
    else:
        form = UpdateCustomerStageForm(instance=customer)
    
    return render(request, 'webapp/update_customer_stage.html', {'form': form, 'customer': customer})


@login_required(login_url='login')
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if not can_access_customer(request.user, customer) and not PermissionGrant.objects.filter(granted_to=request.user, permission='delete').exists():
        return redirect('sales_dashboard')
    
    # Decrease monthly acquisitions
    today = timezone.now()
    stats = MonthlySalesStatistics.objects.filter(
        sales_rep=customer.sales_rep,
        year=today.year,
        month=today.month
    ).first()
    if stats and stats.customers_acquired > 0:
        stats.customers_acquired -= 1
        stats.save()

    customer.delete()
    messages.error(request, 'Customer deleted.')
    
    # Redirect based on user role
    if is_team_leader(request.user):
        return redirect('team_leader_dashboard')
    return redirect('sales_dashboard')


# ============ OWNER DASHBOARD ============

@login_required(login_url='login')
def owner_dashboard(request):
    if not is_owner(request.user):
        return redirect('home')
    
    pending_approvals = UserRole.objects.filter(is_approved=False).select_related('user')
    approved_users = UserRole.objects.filter(is_approved=True).select_related('user')
    team_leaders = approved_users.filter(role='team_leader')
    sales_reps = approved_users.filter(role='sales')
    
    total_customers = Customer.objects.count()
    total_contracts = Customer.objects.filter(current_stage='contract_signed').count()
    
    query = request.GET.get('q', '')
    search_results_users = []
    search_results_customers = []
    
    if query:
        search_results_users = UserRole.objects.filter(
            Q(user__username__icontains=query) | 
            Q(user__first_name__icontains=query) |
            Q(phone__icontains=query),
            is_approved=True
        ).select_related('user')
        
        search_results_customers = Customer.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query)
        )

    context = {
        'pending_approvals': pending_approvals,
        'team_leaders': team_leaders,
        'sales_reps': sales_reps,
        'total_customers': total_customers,
        'total_contracts': total_contracts,
        'now': timezone.now(),
        'query': query,
        'search_results_users': search_results_users,
        'search_results_customers': search_results_customers,
    }
    
    return render(request, 'webapp/owner_dashboard.html', context)


@login_required(login_url='login')
def approve_user(request, user_id):
    if not is_owner(request.user):
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    user_role = user.user_role
    user_role.is_approved = True
    user_role.save()
    
    messages.success(request, f'{user.username} approved as {user_role.get_role_display()}!')
    return redirect('owner_dashboard')


@login_required(login_url='login')
def assign_sales_to_leader(request, sales_id, leader_id):
    if not is_owner(request.user):
        return redirect('home')
    
    sales_user = get_object_or_404(User, id=sales_id)
    leader_user = get_object_or_404(User, id=leader_id)
    
    mapping, created = SalesTeamMapping.objects.get_or_create(sales=sales_user)
    mapping.team_leader = leader_user
    mapping.save()
    
    messages.success(request, f'{sales_user.username} assigned to {leader_user.username}!')
    return redirect('owner_dashboard')


def custom_page_not_found_view(request, exception):
    return render(request, 'webapp/404.html', status=404)


# ============ PASSWORD RESET ============

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


@login_required(login_url='login')
def reset_password(request, user_id):
    if not is_owner(request.user) and not PermissionGrant.objects.filter(granted_to=request.user, permission='reset_password').exists():
        return redirect('home')
    
    user_to_reset = get_object_or_404(User, id=user_id)
    new_password = generate_random_password()
    user_to_reset.set_password(new_password)
    user_to_reset.save()
    
    return render(request, 'webapp/password_reset_complete.html', {
        'user_to_reset': user_to_reset,
        'new_password': new_password,
    })


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')
        
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')
        
        if len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('change_password')
        
        request.user.set_password(new_password1)
        request.user.save()
        
        messages.success(request, 'Password changed successfully! Please log in again.')
        return redirect('logout')
    
    return render(request, 'webapp/change_password.html')


# ============ USER MANAGEMENT ============

@login_required(login_url='login')
def edit_user(request, user_id):
    if not is_owner(request.user) and not PermissionGrant.objects.filter(granted_to=request.user, permission='edit').exists():
        return redirect('home')
    
    user_to_edit = get_object_or_404(User, id=user_id)
    role = get_user_role(user_to_edit)
    
    from .forms import EditSalesRepForm, EditTeamLeaderForm, EditUserForm
    
    if role == 'sales':
        FormClass = EditSalesRepForm
    elif role == 'team_leader':
        FormClass = EditTeamLeaderForm
    else:
        FormClass = EditUserForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=user_to_edit)
        if form.is_valid():
            user = form.save()
            try:
                user_role = user.user_role
                phone = form.cleaned_data.get('phone')
                if phone is not None:
                    user_role.phone = phone
                if role == 'team_leader' and 'team_number' in form.cleaned_data:
                    user_role.team_number = form.cleaned_data.get('team_number')
                user_role.save()
            except UserRole.DoesNotExist:
                pass
            
            if role == 'sales' and 'team_leader' in form.cleaned_data:
                team_leader = form.cleaned_data.get('team_leader')
                mapping, created = SalesTeamMapping.objects.get_or_create(sales=user)
                mapping.team_leader = team_leader
                mapping.save()
            
            messages.success(request, f'{user.username} has been updated successfully!')
            
            if role == 'sales':
                return redirect('sales_reps_list')
            elif role == 'team_leader':
                return redirect('team_leaders_list')
            return redirect('owner_dashboard')
    else:
        form = FormClass(instance=user_to_edit)
    
    return render(request, 'webapp/edit_user.html', {
        'form': form,
        'user_to_edit': user_to_edit,
        'role': role,
    })


@login_required(login_url='login')
def promote_user(request, user_id):
    if not is_owner(request.user):
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    user_role = user.user_role
    
    if user_role.role == 'sales':
        user_role.role = 'team_leader'
        user_role.save()
        SalesTeamMapping.objects.filter(sales=user).delete()
        messages.success(request, f'{user.username} has been promoted to Team Leader!')
        return redirect('team_leaders_list')
    else:
        messages.error(request, 'Only Sales Representatives can be promoted.')
        return redirect('owner_dashboard')


@login_required(login_url='login')
def downgrade_user(request, user_id):
    if not is_owner(request.user):
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    user_role = user.user_role
    
    if user_role.role == 'team_leader':
        user_role.role = 'sales'
        user_role.save()
        SalesTeamMapping.objects.filter(team_leader=user).update(team_leader=None)
        messages.success(request, f'{user.username} has been downgraded to Sales Representative.')
        return redirect('sales_reps_list')
    else:
        messages.error(request, 'Only Team Leaders can be downgraded.')
        return redirect('owner_dashboard')


@login_required(login_url='login')
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    is_self_delete = user_to_delete == request.user

    if not is_self_delete and not is_owner(request.user) and not PermissionGrant.objects.filter(granted_to=request.user, permission='delete').exists():
        return redirect('home')
    
    next_page = request.GET.get('next', 'owner_dashboard')
    
    if request.method == 'POST':
        username = user_to_delete.username
        
        if is_self_delete:
            logout(request)
        
        user_to_delete.delete()
        messages.success(request, f'User {username} has been deleted successfully!')
        
        if is_self_delete:
            return redirect('home')
        elif next_page == 'team_leader_detail':
            return redirect('team_leaders_list')
        elif next_page == 'sales_rep_detail':
            return redirect('sales_reps_list')
        return redirect('owner_dashboard')
    
    return render(request, 'webapp/delete_user.html', {
        'user_to_delete': user_to_delete,
        'next_page': next_page,
    })

@login_required(login_url='login')
def create_user(request):
    if not (is_owner(request.user) or is_team_leader(request.user)):
        return redirect('home')
    
    is_tl = is_team_leader(request.user)
    role_param = request.GET.get('role', 'sales') if is_owner(request.user) else 'sales'
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            role = form.cleaned_data.get('role')
            phone = form.cleaned_data.get('phone')
            team_number = form.cleaned_data.get('team_number', '')
            
            # Team leaders can only create sales, not team leaders
            if is_tl and role != 'sales':
                messages.error(request, 'Team leaders can only create sales representatives.')
                user.delete()
                return redirect('create_user')
            
            UserRole.objects.create(user=user, role=role, phone=phone, team_number=team_number, is_approved=True)
            
            # If team leader creates a sales rep, auto-assign to their team
            if is_tl and role == 'sales':
                SalesTeamMapping.objects.create(sales=user, team_leader=request.user)
                messages.success(request, f'Sales Representative {user.username} created and assigned to your team!')
                return redirect('team_leader_dashboard')
            
            messages.success(request, f'User {user.username} created successfully!')
            if role == 'team_leader':
                return redirect('team_leaders_list')
            return redirect('sales_reps_list')
        else:
            messages.error(request, 'Creation failed. Please check the form.')
    else:
        form = RegisterForm(initial={'role': role_param})
    
    return render(request, 'webapp/create_user.html', {
        'form': form,
        'title': _('Add Sales Representative') if is_tl else (_('Add Team Leader') if role_param == 'team_leader' else _('Add Sales Representative')),
        'role_param': role_param,
        'is_team_leader': is_tl
    })


@login_required(login_url='login')
def team_leaders_list(request):
    if not is_owner(request.user):
        return redirect('home')
    
    team_leaders = UserRole.objects.filter(role='team_leader', is_approved=True)
    return render(request, 'webapp/team_leaders_list.html', {'team_leaders': team_leaders})


@login_required(login_url='login')
def sales_reps_list(request):
    if not is_owner(request.user):
        return redirect('home')
    
    sales_reps = UserRole.objects.filter(role='sales', is_approved=True)
    return render(request, 'webapp/sales_reps_list.html', {'sales_reps': sales_reps})


@login_required(login_url='login')
def customers_list(request):
    if not is_owner(request.user):
        return redirect('home')
    
    customers = Customer.objects.all().order_by('-created_at')
    total_customers = customers.count()
    contracts_signed = customers.filter(current_stage='contract_signed').count()
    in_progress = total_customers - contracts_signed
    danger_zone = sum(1 for c in customers if c.is_in_danger_zone())
    
    return render(request, 'webapp/customers_list.html', {
        'customers': customers,
        'total_customers': total_customers,
        'contracts_signed': contracts_signed,
        'in_progress': in_progress,
        'danger_zone': danger_zone,
    })


@login_required(login_url='login')
def admin_create_customer(request):
    if not is_owner(request.user):
        return redirect('home')
    
    if request.method == 'POST':
        form = AdminCreateCustomerForm(request.POST)
        sales_rep_id = request.POST.get('sales_rep')
        
        if form.is_valid() and sales_rep_id:
            customer = form.save(commit=False)
            customer.sales_rep = get_object_or_404(User, id=sales_rep_id)
            customer.save()
            messages.success(request, f'Customer {customer.first_name} added and assigned successfully!')
            return redirect('customers_list')
        else:
            messages.error(request, 'Failed to add customer. Please check the form.')
    else:
        form = AdminCreateCustomerForm()
    
    sales_reps = User.objects.filter(
        Q(user_role__role__in=['sales', 'team_leader'], user_role__is_approved=True) |
        Q(id=request.user.id)
    ).select_related('user_role').order_by('user_role__role', 'username')
    return render(request, 'webapp/admin_create_customer.html', {
        'form': form,
        'sales_reps': sales_reps,
        'title': 'Add New Customer (Admin)',
    })


@login_required(login_url='login')
def danger_zone_list(request):
    if not is_owner(request.user):
        return redirect('home')
    
    all_customers = Customer.objects.all()
    danger_customers = [c for c in all_customers if c.is_in_danger_zone()]
    return render(request, 'webapp/danger_zone_list.html', {
        'customers': danger_customers,
        'total_danger': len(danger_customers),
    })

@login_required(login_url='login')
def sales_rep_detail(request, user_id):
    if not is_owner(request.user) and not is_team_leader(request.user):
        return redirect('home')
    
    sales_user = get_object_or_404(User, id=user_id)
    sales_role = get_object_or_404(UserRole, user=sales_user)
    customers = Customer.objects.filter(sales_rep=sales_user).order_by('-created_at')
    
    return render(request, 'webapp/sales_rep_detail.html', {
        'sales_user': sales_user,
        'sales_role': sales_role,
        'customers': customers,
        'from_leader': request.GET.get('from_leader'),
    })


@login_required(login_url='login')
def team_leader_detail(request, user_id):
    if not is_owner(request.user):
        return redirect('home')
    
    leader_user = get_object_or_404(User, id=user_id)
    leader_role = get_object_or_404(UserRole, user=leader_user)
    sales_members = leader_user.sales_members.all()
    
    sales_with_customers = []
    for mapping in sales_members:
        sales_user = mapping.sales
        customers = Customer.objects.filter(sales_rep=sales_user).order_by('-created_at')
        sales_with_customers.append({
            'user': sales_user,
            'customers': customers,
            'customer_count': customers.count()
        })
    
    leader_own_customers = Customer.objects.filter(sales_rep=leader_user).order_by('-created_at')
    
    return render(request, 'webapp/team_leader_detail.html', {
        'leader_user': leader_user,
        'leader_role': leader_role,
        'sales_with_customers': sales_with_customers,
        'leader_own_customers': leader_own_customers,
        'total_sales': sales_members.count(),
    })

@login_required(login_url='login')
def manage_permissions(request, user_id):
    if not is_owner(request.user):
        return redirect('home')
    
    target_user = get_object_or_404(User, id=user_id)
    all_permissions = ['edit', 'reset_password', 'delete']
    
    if request.method == 'POST':
        selected = request.POST.getlist('permissions')
        PermissionGrant.objects.filter(granted_to=target_user).delete()
        for perm in selected:
            if perm in all_permissions:
                PermissionGrant.objects.create(granted_to=target_user, permission=perm)
        messages.success(request, f'Permissions updated for {target_user.username}!')
        return redirect(request.POST.get('next', 'owner_dashboard'))
    
    current_permissions = list(
        PermissionGrant.objects.filter(granted_to=target_user).values_list('permission', flat=True)
    )
    
    return render(request, 'webapp/manage_permissions.html', {
        'target_user': target_user,
        'all_permissions': all_permissions,
        'current_permissions': current_permissions,
    })

@login_required(login_url='login')
def reject_user(request, user_id):
    if not is_owner(request.user):
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f'{username} has been rejected and removed.')
    return redirect('owner_dashboard')

@login_required(login_url='login')
def final_agreement_list(request):
    if not is_owner(request.user):
        return redirect('home')
    
    customers = Customer.objects.filter(current_stage='contract_signed').order_by('-updated_at')
    return render(request, 'webapp/filtered_customers_list.html', {
        'customers': customers,
        'title': _('Final Agreement Customers'),
        'subtitle': _('Customers who have signed contracts'),
        'theme_color': '#28a745',
    })

@login_required(login_url='login')
def in_progress_list(request):
    if not is_owner(request.user):
        return redirect('home')
    
    customers = Customer.objects.exclude(current_stage='contract_signed').order_by('-created_at')
    return render(request, 'webapp/filtered_customers_list.html', {
        'customers': customers,
        'title': _('In Progress Customers'),
        'subtitle': _('Customers currently moving through the pipeline'),
        'theme_color': '#17a2b8',
    })