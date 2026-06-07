from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    UserRole, Customer, SalesTeamMapping, 
    CustomerStageHistory, MonthlySalesStatistics, PermissionGrant
)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_approved', 'created_at')
    list_filter = ('role', 'is_approved')
    search_fields = ('user__username',)
    actions = ['grant_edit_permission', 'grant_reset_password_permission', 'grant_delete_permission']

    def grant_edit_permission(self, request, queryset):
        for user_role in queryset:
            user = user_role.user
            PermissionGrant.objects.get_or_create(granted_to=user, permission='edit')
        self.message_user(request, "Edit permission granted to selected users.")
    grant_edit_permission.short_description = "Grant Edit permission to selected users"

    def grant_reset_password_permission(self, request, queryset):
        for user_role in queryset:
            user = user_role.user
            PermissionGrant.objects.get_or_create(granted_to=user, permission='reset_password')
        self.message_user(request, "Reset password permission granted to selected users.")
    grant_reset_password_permission.short_description = "Grant Reset Password permission to selected users"

    def grant_delete_permission(self, request, queryset):
        for user_role in queryset:
            user = user_role.user
            PermissionGrant.objects.get_or_create(granted_to=user, permission='delete')
        self.message_user(request, "Delete permission granted to selected users.")
    grant_delete_permission.short_description = "Grant Delete permission to selected users"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'sales_rep', 'current_stage', 'created_at')
    list_filter = ('current_stage', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'stage_start_date')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'

@admin.register(SalesTeamMapping)
class SalesTeamMappingAdmin(admin.ModelAdmin):
    list_display = ('sales', 'team_leader', 'assigned_date')
    search_fields = ('sales__username', 'team_leader__username')

@admin.register(CustomerStageHistory)
class CustomerStageHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'previous_stage', 'new_stage', 'changed_at')
    list_filter = ('changed_at',)

@admin.register(MonthlySalesStatistics)
class MonthlySalesStatisticsAdmin(admin.ModelAdmin):
    list_display = ('sales_rep', 'year', 'month', 'customers_acquired', 'contracts_signed')
    list_filter = ('year', 'month')

@admin.register(PermissionGrant)
class PermissionGrantAdmin(admin.ModelAdmin):
    list_display = ['granted_to', 'permission']
    list_filter = ['permission']