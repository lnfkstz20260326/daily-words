# -*- coding: utf-8 -*-
"""
彻底清理HTML结构问题
- 修复损坏的HTML标签
- 删除重复内容
- 确保结构完整
"""

import os
import glob
import re

def fix_html_file(filepath):
    """修复单个HTML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # =========================================
    # 修复1: 删除所有在 </div> 后面的损坏内容
    # 找到第5个card的结束标签，删除之后的所有损坏内容
    # =========================================
    
    # 模式：第5个card结束后，查找损坏的内容
    # 删除从 "我需要新衣服" 的重复例句开始的所有损坏内容
    damaged_pattern = r'<div class="memory-tip">[^<]*</div><div class="loop-status"[^>]*>[^<]*</div>\s*<div class="nav-links">[^<]*<a[^>]*>← 前一天</a>[^<]*<a[^>]*>📅 返回首页</a>[^<]*<a href：拆开记：[^<]*'
    
    # 正确的结构应该是：
    # </div> (card结束)
    # <div class="loop-status">...</div>
    # <div class="nav-links">...</div>
    # </div> (container结束)
    # <script>...</script>
    # </body></html>
    
    # 替换为正确的内容
    replacement = '<div class="memory-tip">💡 记忆小提示：cloth=布料，-es=复数，布料做的衣物总称</div>\n        </div>\n\n        <div class="loop-status" id="loopStatus">\n            🔄 点击卡片下方按钮开始朗读 · 页面加载3秒后自动循环播放\n        </div>\n\n        <div class="nav-links">\n            <a href="index.html">← 前一天</a>\n            <a href="index.html">📅 返回首页</a>\n            <a href="2026-04-01.html">明天 →</a>\n        </div>\n    </div>\n'
    
    new_content = re.sub(damaged_pattern, replacement, content)
    
    # =========================================
    # 修复2: 删除第二个损坏的 loop-status 和 nav-links
    # =========================================
    second_damaged = r'<div class="loop-status" id="loopstatus">[^<]*</div>\s*<div class="nav-links">[^<]*<a[^>]*>← 前一天</a>[^<]*<a[^>]*>📅 返回首页</a>[^<]*<a href\s*</div>\s*'
    new_content = re.sub(second_damaged, '', new_content)
    
    if new_content != content:
        content = new_content
        modified = True
    
    # =========================================
    # 修复3: 修复第二个重复的 nav-links
    # =========================================
    # 确保只有一个 nav-links 在正确位置
    
    # =========================================
    # 修复4: 确保 nav-links 中的第三个链接 href 属性正确
    # =========================================
    # 查找 href 属性值是 "2026-xx-xx.html" 的部分
    # 目前是 <a href="index.html">明天 →</a>，应该改成对应的日期
    
    # 由于静态文件无法自动计算前一天和后一天，
    # 暂时都指向 index.html
    
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
