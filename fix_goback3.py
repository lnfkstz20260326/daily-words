#!/usr/bin/env python3
"""
修复 goBack() 函数 - 在跳转前确保音频停止
使用正则表达式处理任意缩进
"""
import os
import re
import glob

# 正则匹配 goBack 函数（任意缩进）
pattern = r'([ \t]*)function goBack\(\) \{[\s\S]*?window\.location\.href = \'index\.html\';[\s\S]*?\}'

# 新代码模板
new_code_template = '''{indent}function goBack() {{
            // 先停止所有语音播放
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;

            // 等待音频真正停止后再跳转
            setTimeout(() => {{
                window.location.href = 'index.html';
            }}, 100);
        }}'''

count = 0
fixed = 0

for filepath in sorted(glob.glob('[0-9][0-9][0-9][0-9]-*.html')):
    count += 1
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否需要修复
    if 'setTimeout(() => {' not in content:
        match = re.search(pattern, content)
        if match:
            indent = match.group(1)
            new_code = new_code_template.format(indent=indent)
            new_content = content[:match.start()] + new_code + content[match.end():]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
            print(f"Fixed: {filepath}")

print(f"\nTotal: {count}, Fixed: {fixed}")
