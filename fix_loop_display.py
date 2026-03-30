import os
import re
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 检查所有HTML文件中的轮数显示代码
problems = []
for f in sorted(glob.glob('2026-*.html')):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        # 检查轮数显示的方式
        m = re.search(r"statusDiv\.textContent\s*=\s*([`'\"])", content)
        quote_type = m.group(1) if m else None
        if quote_type == "'":
            problems.append((f, "使用单引号"))
        elif quote_type == '"':
            problems.append((f, "使用双引号"))
        elif quote_type == '`':
            pass  # 正确
        else:
            problems.append((f, "无法确定引号类型"))
        
        # 检查变量定义
        if not re.search(r'(let|var)\s+currentLoop\s*=', content):
            problems.append((f, "缺少currentLoop变量定义"))
        if not re.search(r'(let|const|var)\s+maxLoops\s*=\s*\d+', content):
            problems.append((f, "缺少maxLoops变量定义"))

if problems:
    print(f"发现问题 {len(problems)} 个:")
    for p in problems[:20]:
        print(f"  {p[0]}: {p[1]}")
else:
    print("所有文件格式正确")
