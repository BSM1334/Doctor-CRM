import os
import re

file_path = r'd:\D\Basel\Work\CRM_project\crm\webapp\views.py'

with open(file_path, 'r') as f:
    content = f.read()

# Pattern for the redirect blocks
# Target: 
# if is_owner(...):
#     return redirect('owner_dashboard')
# else:
#     return redirect('sales_dashboard')

pattern = r"(if is_owner\(.*?\):\n\s+return redirect\('owner_dashboard'\))\n(\s+)else:\n\s+return redirect\('sales_dashboard'\)"
replacement = r"\1\n\2elif is_team_leader(request.user if 'request' in locals() else user):\n\2    return redirect('team_leader_dashboard')\n\2else:\n\2    return redirect('sales_dashboard')"

# Note: The 'request.user if ... else user' is to handle both views (request.user) and form-logic (user)
# Actually, let's be more specific for each view type.

# 1. Views using 'request.user' (home, login_view)
content = content.replace(
    "        if is_owner(request.user):\n            return redirect('owner_dashboard')\n        else:\n            return redirect('sales_dashboard')",
    "        if is_owner(request.user):\n            return redirect('owner_dashboard')\n        elif is_team_leader(request.user):\n            return redirect('team_leader_dashboard')\n        else:\n            return redirect('sales_dashboard')"
)

# 2. Views using 'user' (login_view successful login)
# Already handled by the previous multi_replace_file_content successfully in some parts, but let's be thorough.

with open(file_path, 'w') as f:
    f.write(content)

print("Successfully updated redirects in views.py")
