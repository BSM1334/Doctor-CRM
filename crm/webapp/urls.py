from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('owner-login/', views.owner_login, name='owner_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Sales & Team Leader Dashboards
    path('sales-dashboard/', views.sales_dashboard, name='sales_dashboard'),
    path('team-leader-dashboard/', views.team_leader_dashboard, name='team_leader_dashboard'),
    
    # Customer Management
    path('customer/create/', views.create_customer, name='create_customer'),
    path('customer/<int:customer_id>/', views.view_customer, name='view_customer'),
    path('customer/<int:customer_id>/update/', views.update_customer, name='update_customer'),
    path('customer/<int:customer_id>/stage/', views.update_customer_stage, name='update_customer_stage'),
    path('customer/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),
    
    # Owner Dashboard
    path('owner-dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('assign-sales/<int:sales_id>/to/<int:leader_id>/', views.assign_sales_to_leader, name='assign_sales'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('promote-user/<int:user_id>/', views.promote_user, name='promote_user'),
    path('downgrade-user/<int:user_id>/', views.downgrade_user, name='downgrade_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('create-user/', views.create_user, name='create_user'),
    path('team-leaders/', views.team_leaders_list, name='team_leaders_list'),
    path('sales-representatives/', views.sales_reps_list, name='sales_reps_list'),
    path('customers-list/', views.customers_list, name='customers_list'),
    path('customer/admin-create/', views.admin_create_customer, name='admin_create_customer'),
    path('danger-zone/', views.danger_zone_list, name='danger_zone_list'),
    path('customers/final/', views.final_agreement_list, name='final_agreement_list'),
    path('customers/in-progress/', views.in_progress_list, name='in_progress_list'),
    path('sales-representative/<int:user_id>/', views.sales_rep_detail, name='sales_rep_detail'),
    path('team-leader/<int:user_id>/', views.team_leader_detail, name='team_leader_detail'),
    path('reject-user/<int:user_id>/', views.reject_user, name='reject_user'),
    
    # Password Management
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('manage-permissions/<int:user_id>/', views.manage_permissions, name='manage_permissions'),
    
    # PWA files
    path('manifest.json', TemplateView.as_view(template_name='webapp/manifest.json', content_type='application/json'), name='manifest'),
    path('sw.js', TemplateView.as_view(template_name='webapp/sw.js', content_type='application/javascript'), name='service_worker'),
]
