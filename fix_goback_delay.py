#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 goBack() 函数 - 增加延迟时间到500ms
"""
import os
import re
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

count = 0
fixed = 0

for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    count += 1
    filepath = os.path.join('.', filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否是旧的100ms
    if "setTimeout(() => {\n                window.location.href = 'index.html';\n            }, 100);" in content:
        new_content = content.replace(', 100);', ', 500);')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f"Fixed delay: {filename}")

print(f"\nTotal: {count}, Fixed: {fixed}")
