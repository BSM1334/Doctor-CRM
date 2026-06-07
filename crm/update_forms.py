import os
import re

filepath = r'd:\D\Basel\Work\CRM_project\crm\webapp\forms.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the import statement
if 'from django.utils.translation import gettext_lazy as _' not in content:
    content = content.replace('from django.forms.widgets import', 'from django.utils.translation import gettext_lazy as _\nfrom django.forms.widgets import')

content = content.replace("help_text=\"Format: + [Country Code] [Number]\"", "help_text=_('Format: + [Country Code] [Number]')")
content = content.replace("help_text=\"Select your designation in the company\"", "help_text=_('Select your designation in the company')")
content = content.replace("label=\"Name\"", "label=_('Name')")
content = content.replace("label=\"Phone Number\"", "label=_('Phone Number')")
content = content.replace("label=\"Team Leader\"", "label=_('Team Leader')")
content = content.replace("help_text=\"Number of days the customer has already been in this stage.\"", "help_text=_('Number of days the customer has already been in this stage.')")

# Add labels for User forms
content = content.replace("        labels = {\n            'username': 'Name',\n        }", "        labels = {\n            'username': _('Name'),\n        }")
content = content.replace("        labels = {\n            'sales_rep': 'Sales',\n        }", "        labels = {\n            'sales_rep': _('Sales'),\n        }")

# Add a Meta labels section to CreateCustomerForm, AdminCreateCustomerForm, UpdateCustomerStageForm, EditUserForm
# Wait, for ModelForms without explicitly defined fields, Django uses the model's verbose_name.
# It is better to just define the labels for all ModelForms right in the forms.py.

meta_pattern_create_customer = r"(class CreateCustomerForm\(forms\.ModelForm\):.*?class Meta:.*?widgets = \{.*?\n        \})"
labels_for_customer = """
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone': _('Phone'),
            'request': _('Request'),
            'current_stage': _('Current Stage'),
            'sales_rep': _('Sales'),
        }"""
        
meta_pattern_admin_customer = r"(class AdminCreateCustomerForm\(forms\.ModelForm\):.*?class Meta:.*?widgets = \{.*?\n        \})"
meta_pattern_update_customer = r"(class UpdateCustomerForm\(forms\.ModelForm\):.*?class Meta:.*?widgets = \{.*?\n        \})"

content = re.sub(meta_pattern_create_customer, r"\1" + labels_for_customer, content, flags=re.DOTALL)

# Because we did a global replace or specific, let's just make sure we add labels correctly.
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Forms updated with gettext_lazy')
