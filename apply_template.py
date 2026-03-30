# -*- coding: utf-8 -*-
"""
应用模板脚本 - 使用2026-04-01.html作为模板同步所有文件
保留每个文件原有的数据（词汇、日期等）
"""

import glob
import re

# 读取模板
with open('2026-04-01.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 提取模板中的关键部分
# 1. 样式部分（从<style>到</style>）
style_match = re.search(r'(<style>.*?</style>)', template, re.DOTALL)
template_style = style_match.group(1) if style_match else None

# 2. top-controls HTML
top_controls_match = re.search(r'(<div class="top-controls">.*?</div>\s*)', template, re.DOTALL)
template_top_controls = top_controls_match.group(1) if top_controls_match else None

# 3. 循环状态和导航
loop_status_match = re.search(r'(<div class="loop-status".*?</div>\s*<div class="nav-links">.*?</div>\s*)', template, re.DOTALL)
template_footer = loop_status_match.group(1) if loop_status_match else None

# 4. JS脚本
script_match = re.search(r'(<script>.*?</script>)', template, re.DOTALL)
template_script = script_match.group(1) if script_match else None

print("Template parts extracted:")
print(f"  Style: {bool(template_style)}")
print(f"  Top controls: {bool(template_top_controls)}")
print(f"  Footer: {bool(template_footer)}")
print(f"  Script: {bool(template_script)}")


def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果文件已经是正确格式，跳过
    if 'top-controls' in content and '// 点击卡片按钮时' in content:
        return False
    
    original = content
    modified = False
    
    # 1. 更新样式部分
    if template_style:
        content = re.sub(r'<style>.*?</style>', template_style, content, flags=re.DOTALL)
        modified = True
    
    # 2. 替换top-controls
    if template_top_controls:
        # 删除现有的top-controls（无论在哪里）
        content = re.sub(r'\s*<div class="top-controls">.*?</div>\s*', '\n', content, flags=re.DOTALL)
        # 在header结束后添加
        pattern = r'(<div class="grade">.*?</div>\s*</div>\s*)'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1\n\n' + template_top_controls, content)
            modified = True
    
    # 3. 更新底部循环状态和导航
    if template_footer:
        content = re.sub(r'<div class="loop-status".*?</div>\s*<div class="nav-links">.*?</div>\s*', 
                        template_footer, content, flags=re.DOTALL)
        modified = True
    
    # 4. 更新JS脚本
    if template_script:
        content = re.sub(r'<script>.*?</script>', template_script, content, flags=re.DOTALL)
        modified = True
    
    if modified:
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
