import os
import re
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 查找所有使用单引号或双引号的轮数显示行
for f in sorted(glob.glob('2026-*.html'))[:10]:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        # 查找 statusDiv.textContent 相关的行
        matches = re.findall(r'.{0,30}第.+\{currentLoop\}.+轮.{0,30}', content)
        if matches:
            print(f'{f}:')
            for m in matches:
                print(f'  {m}')
