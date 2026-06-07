import os

directory = r'd:\D\Basel\Work\CRM_project\crm\webapp\templates\webapp'

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            new_content = content.replace('<bdi>', '<bdi dir="ltr">')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Fixed {file}')
