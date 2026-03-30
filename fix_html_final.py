# -*- coding: utf-8 -*-
"""
彻底修复HTML结构 - 删除所有损坏的重复内容
"""

import glob
import re

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # =========================================
    # 策略：找到最后一个 </div> (card结束) 之后的所有内容
    # 替换为正确的结尾
    # =========================================
    
    # 找到第5个card结束的位置（最后一个card）
    # 匹配 </div> 后面跟着 <div class="loop-status">
    # 但这是在损坏内容之前
    
    # 更简单的方法：删除从损坏的 <a href：开始到文件结尾的所有内容
    # 然后添加正确的结尾
    
    # 删除损坏内容：从 '<a href：拆开记：' 开始到文件结束
    damaged_start = '<a href：拆开记：'
    
    if damaged_start in content:
        # 找到这个位置
        idx = content.find(damaged_start)
        # 找到它前面的 <div class="nav-links"> 或 <div class="loop-status">
        # 向前查找最近的 <div class="loop-status"
        loop_status_idx = content.rfind('<div class="loop-status"', 0, idx)
        if loop_status_idx == -1:
            loop_status_idx = content.rfind('<div class="loop-status"', 0, idx)
        
        if loop_status_idx != -1:
            # 删除从loop-status开始的所有内容
            content = content[:loop_status_idx]
            modified = True
    
    # 添加正确的结尾
    if modified and not content.endswith('</div>\n'):
        # 确保有正确的结尾
        if not content.strip().endswith('</div>'):
            content = content.rstrip() + '\n'
        
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
        
        # 检查是否已经以 </div> 结束
        if '</div>\n\n    <div class="loop-status"' not in content:
            content = content.rstrip() + '\n        </div>\n' + correct_ending
    
    # 另一种情况：如果内容以 </div> 结束
    if content.endswith('</div>\n'):
        # 检查是否已经包含 loop-status 和 nav-links
        if '<div class="loop-status"' not in content or '<div class="nav-links"' not in content:
            # 找到最后一个 </div>
            last_div_idx = content.rfind('</div>')
            if last_div_idx != -1:
                content = content[:last_div_idx + 6] + '''
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
                modified = True
    
    # 还需要处理 script 部分之前的内容
    # 如果 script 标签已经存在，确保它在正确位置
    
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
