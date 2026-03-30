#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 goBack() 函数 - 在跳转前确保音频停止
"""
import os
import re
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 新代码
NEW_CODE = '''function goBack() {
            // 先停止所有语音播放
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;

            // 等待音频真正停止后再跳转
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 100);
        }'''

count = 0
fixed = 0

for filename in os.listdir('.'):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    count += 1
    filepath = os.path.join('.', filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否需要修复
    if 'setTimeout(() => {' in content:
        continue
    
    # 查找 goBack 函数并替换 - 匹配整个函数体
    pattern = r'function goBack\(\) \{[^}]+speechSynthesis\.cancel\(\);[^}]+window\.location\.href = \'index\.html\';[^}]+\}'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = content[:match.start()] + NEW_CODE + content[match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f"Fixed: {filename}")

print(f"\nTotal: {count}, Fixed: {fixed}")
