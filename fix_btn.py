#!/usr/bin/env python3
import os, re

count = 0
for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    filepath = os.path.join('.', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if ".btn-primary'" in content:
        content = content.replace(".btn-primary'", ".btn-loop'")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f'Fixed btn selector: {filename}')

print(f'\nTotal: {count} files fixed')
