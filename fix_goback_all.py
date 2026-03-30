#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有文件的 goBack() 函数 - 添加 setTimeout
"""
import os
import re
import sys

# 设置输出编码
sys.stdout = __import__('codecs').getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 旧的 goBack 函数模式
OLD_FUNC = '''function goBack() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            const statusEl = document.getElementById('loopStatus');
            const btnEl = document.getElementById('loopBtn');
            if (statusEl) statusEl.textContent = '⏹ 已停止';
            if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
            window.location.href = 'index.html';
        }'''

# 新代码 - 添加 setTimeout 延迟
NEW_FUNC = '''function goBack() {
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
    
    # 检查是否需要修复 - 查找 goBack 函数中是否有 setTimeout
    # 简单检查：如果 goBack 函数里有 window.location.href = 'index.html' 且前面没有 setTimeout
    if "window.location.href = 'index.html';" not in content:
        continue
    
    # 查找 goBack 函数
    match = re.search(r'(function goBack\(\) \{[^}]+window\.location\.href = \'index\.html\';[^}]+\})', content, re.DOTALL)
    if match and 'setTimeout' not in match.group():
        new_content = content.replace(match.group(), NEW_FUNC)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
        print(f"Fixed: {filename}")

print(f"\nTotal: {count}, Fixed: {fixed}")
