# -*- coding: utf-8 -*-
"""
应用模板脚本 v2 - 确保top-controls在正确位置
"""

import glob
import re

# 读取模板
with open('2026-04-01.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 提取top-controls HTML
top_controls_match = re.search(r'(<div class="top-controls">.*?</div>\s*)', template, re.DOTALL)
template_top_controls = top_controls_match.group(1) if top_controls_match else None


def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    if not template_top_controls:
        return False
    
    # 1. 删除所有现有的top-controls（无论在哪里）
    content = re.sub(r'\s*<div class="top-controls">.*?</div>\s*', '\n', content, flags=re.DOTALL)
    
    # 2. 在header结束后添加top-controls
    # 匹配 </div> 后面跟着空白和 <div class="card">
    pattern = r'(<div class="grade">.*?</div>\s*</div>\s*)(\s*<div class="card">)'
    replacement = r'\1\n\n' + template_top_controls + r'\2'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        content = new_content
        modified = True
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return modified


def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    html_files = glob.glob('2026-*.html') + glob.glob('2027-*.html')
    html_files.sort()
    
    fixed_count = 0
    for filepath in html_files:
        if fix_html_file(filepath):
            fixed_count += 1
            print(f"[OK] {filepath}")
    
    print(f"\nTotal: Fixed {fixed_count} files")


if __name__ == '__main__':
    main()
