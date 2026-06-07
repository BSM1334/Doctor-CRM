import re

filepath = r'd:\D\Basel\Work\CRM_project\crm\locale\ar\LC_MESSAGES\django.po'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

translations = {
    'First Name': 'الاسم الأول',
    'Last Name': 'اسم العائلة',
    'Phone': 'رقم الهاتف',
    'Request': 'الطلب',
    'Current Stage': 'المرحلة الحالية',
    'Sales': 'المبيعات',
    'Name': 'الاسم',
    'Phone Number': 'رقم الهاتف',
    'Team Leader': 'قائد الفريق',
    'Format: + [Country Code] [Number]': 'الصيغة: + [رمز الدولة] [الرقم]',
    'Select your designation in the company': 'اختر المسمى الوظيفي في الشركة',
    'Number of days the customer has already been in this stage.': 'عدد الأيام التي قضاها العميل في هذه المرحلة.',
    'Username': 'اسم المستخدم',
    'Password': 'كلمة المرور'
}

for msgid, msgstr in translations.items():
    # Replace empty msgstr for specific msgid
    pattern = r'msgid \"' + re.escape(msgid) + r'\"\nmsgstr \"\"'
    replacement = f'msgid \"{msgid}\"\\nmsgstr \"{msgstr}\"'
    content = re.sub(pattern, replacement, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Translations updated')
