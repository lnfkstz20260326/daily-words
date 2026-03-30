"""修复按钮选择器：.btn-primary -> .btn-loop"""
import os
import re

count = 0
for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复: btn-primary -> btn-loop
    new_content = content.replace("querySelector('.btn-primary')", "querySelector('.btn-loop')")
    
    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f'Fixed: {filename}')

print(f'\nTotal: {count} files fixed')
