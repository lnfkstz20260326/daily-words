#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加 toggleLoop 函数到所有文件
"""
import os
import re
import sys

# 设置输出编码
sys.stdout = __import__('codecs').getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 要添加的代码
NEW_FUNC = '''
        // 切换循环播放状态
        function toggleLoop() {
            const btn = document.getElementById('loopBtn');
            if (isLooping) {
                // 正在播放 -> 停止
                stopSpeaking();
            } else {
                // 未播放 -> 开始播放
                startAutoLoop();
            }
        }

'''

count = 0
fixed = 0

for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    count += 1
    filepath = os.path.join('.', filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否需要添加
    if 'function toggleLoop()' in content:
        continue
    
    # 找到 speakOnce(); 后面的位置
    if 'speakOnce();' in content and 'function stopSpeaking()' in content:
        # 在 speakOnce(); 和 function stopSpeaking() 之间添加
        old_str = '''            speakOnce();
        }

        function stopSpeaking() {'''
        new_str = '''            speakOnce();
        }
''' + NEW_FUNC + '''
        function stopSpeaking() {'''
        
        if old_str in content:
            new_content = content.replace(old_str, new_str)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
            print(f"Fixed: {filename}")

print(f"\nTotal: {count}, Fixed: {fixed}")
