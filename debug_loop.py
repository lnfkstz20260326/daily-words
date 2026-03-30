import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('2026-03-31.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# 查找所有包含 statusDiv.textContent 的行
for i, line in enumerate(content.split('\n')):
    if 'statusDiv' in line and 'textContent' in line:
        # 显示引号类型
        if '`' in line:
            quote = 'backtick'
        elif "'" in line:
            quote = 'single'
        elif '"' in line:
            quote = 'double'
        else:
            quote = 'unknown'
        print(f'Line {i}: quote={quote}')
        # 显示代码片段（去掉emoji避免编码问题）
        clean_line = line.replace('\U0001f504', '?').replace('\u23f9', '?')
        print(f'  {clean_line[:120]}')
