#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有文件的 goBack() 函数 - 使用正则表达式
"""
import os
import re
import sys

# 设置输出编码 - 必须先执行
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 新代码
NEW_CODE = '''function goBack() {
            // 先停止所有语音播放
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            
            // 等待音频真正停止后再跳转（500ms确保语音中断）
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 500);
        }'''

count = 0
fixed = 0

for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    count += 1
    filepath = os.path.join('.', filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否需要修复
    if 'setTimeout(() => {' in content:
        continue
    
    # 使用正则替换 goBack 函数
    pattern = r'function goBack\(\) \{[\s\S]*?window\.location\.href = \'index\.html\';[\s\n]+[\s]*\}[\s]*\n'
    
    match = re.search(pattern, content)
    if match:
        new_content = content[:match.start()] + NEW_CODE + '\n' + content[match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f"Fixed: {filename}")

print(f"\nTotal: {count}, Fixed: {fixed}")
