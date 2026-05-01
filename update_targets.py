import os
import shutil

targets = ['segou', 'bougouni', 'taoudeni', 'tessalit', 'san', 'gao']
css_module_path = 'targets/premium_css.py'

for target in targets:
    target_dir = f'targets/{target}'
    # Copy CSS module
    shutil.copy(css_module_path, f'{target_dir}/premium_css.py')
    
    # Update app.py to use the module
    app_path = f'{target_dir}/app.py'
    if os.path.exists(app_path):
        with open(app_path, 'r') as f:
            content = f.read()
        
        # Replace the open() call with import
        new_content = content.replace("PREMIUM_CSS = open('static/css/targets_premium.css', 'r').read()", "from premium_css import PREMIUM_CSS")
        # Handle cases where I might have used a different path or variable name
        new_content = new_content.replace("PREMIUM_CSS = open('../../static/css/targets_premium.css', 'r').read()", "from premium_css import PREMIUM_CSS")
        
        with open(app_path, 'w') as f:
            f.write(new_content)
    
    # Update Dockerfile to COPY premium_css.py
    dockerfile_path = f'{target_dir}/Dockerfile'
    if os.path.exists(dockerfile_path):
        with open(dockerfile_path, 'r') as f:
            lines = f.readlines()
        
        # Insert COPY premium_css.py . before COPY app.py .
        new_lines = []
        for line in lines:
            if 'COPY app.py .' in line:
                new_lines.append('COPY premium_css.py .\n')
            new_lines.append(line)
        
        with open(dockerfile_path, 'w') as f:
            f.writelines(new_lines)

print("[+] All targets updated successfully!")
