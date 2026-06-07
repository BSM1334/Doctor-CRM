import os
import re

file_path = r'd:\D\Basel\Work\CRM_project\crm\webapp\forms.py'

with open(file_path, 'r') as f:
    content = f.read()

# 1. Add clean_phone to CreateCustomerForm if it doesn't exist
# Look for 'class CreateCustomerForm(forms.ModelForm):' and its Meta class
if "def clean_phone(self):" not in content.split("class CreateCustomerForm")[1].split("class")[0]:
    # We find the end of the Meta class for CreateCustomerForm
    # Meta is at lines 79-100 currently
    target = """            'request': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }"""
    replacement = target + """

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        if UserRole.objects.filter(phone=phone).exists() or Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered in the system.")
        return phone"""
    content = content.replace(target, replacement)

# 2. Update existing clean_phone methods to check BOTH tables
# We want to replace blocks that only check UserRole
old_user_clean = """    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        qs = UserRole.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            qs = qs.exclude(user=self.instance)
        
        if qs.exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone"""

new_user_clean = """    def clean_phone(self):
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
            
        return phone"""

content = content.replace(old_user_clean, new_user_clean)

# Also handle EditTeamLeaderForm which is at the end of the file and might be truncated in my previous view
# I'll check it manually or use regex

with open(file_path, 'w') as f:
    f.write(content)

print("Successfully updated forms.py for global phone uniqueness")
