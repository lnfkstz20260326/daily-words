# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

count = 0
for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复顶部循环按钮 - toggleLoop -> startAutoPlay
    content = content.replace('onclick="toggleLoop()"', 'onclick="startAutoPlay()"')
    
    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f'Fixed: {filename}')

print(f'\nTotal: {count} files fixed')
