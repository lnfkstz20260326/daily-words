# -*- coding: utf-8 -*-
"""
精确修复HTML结构 - 删除损坏内容，保留正常内容
"""

import glob

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # =========================================
    # 删除损坏的重复内容块
    # 损坏从 '<a href：拆开记：' 开始
    # =========================================
    
    damaged_marker = '<a href：拆开记：'
    
    if damaged_marker not in content:
        return False
    
    # 找到损坏内容的位置
    idx = content.find(damaged_marker)
    
    # 向前找到 <div class="nav-links"> 的位置（这是要删除的部分的开头）
    # 但要保留正常的 nav-links 之前的正常内容
    
    # 向前搜索，找到 <div class="loop-status" 或 <div class="nav-links"
    search_start = idx
    while search_start > 0 and '<div class="nav-links"' not in content[max(0, search_start-100):search_start]:
        # 继续向前找
        prev = content.rfind('<div class="loop-status"', 0, search_start)
        if prev == -1:
            prev = content.rfind('<div class="nav-links"', 0, search_start)
        if prev == -1:
            break
        search_start = prev
    
    # 找到 <div class="loop-status" 的位置
    loop_status_idx = content.rfind('<div class="loop-status"', 0, idx)
    nav_links_idx = content.rfind('<div class="nav-links"', 0, idx)
    
    if loop_status_idx == -1 and nav_links_idx == -1:
        return False
    
    # 找到这两个 div 之前最近的正确内容
    # 应该是 </div> (card结束)
    
    # 向后找到 </script> 或 </body>
    script_idx = content.find('<script>', idx)
    
    # 删除从 loop-status/nav-links 开始，到 </script> 之前的所有内容
    if script_idx != -1:
        # 删除这段内容，然后用正确的内容替换
        content = content[:loop_status_idx if loop_status_idx != -1 else nav_links_idx]
        
        # 添加正确的结尾
        correct_ending = '''
        <div class="loop-status" id="loopStatus">
            🔄 点击卡片下方按钮开始朗读 · 页面加载3秒后自动循环播放
        </div>

        <div class="nav-links">
            <a href="index.html">← 前一天</a>
            <a href="index.html">📅 返回首页</a>
            <a href="index.html">明天 →</a>
        </div>
    </div>

    <script>'''
        
        content = content.rstrip() + correct_ending + content[script_idx + 8:]
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False


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
