# -*- coding: utf-8 -*-
"""
同步模板脚本 - 基于2026-03-31.html的结构同步所有文件
"""

import glob
import re

# 读取模板文件
with open('2026-03-31.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 提取模板中的关键部分
# 1. top-controls HTML
top_controls_match = re.search(r'(<div class="top-controls">.*?</div>\s*)', template, re.DOTALL)
top_controls = top_controls_match.group(1) if top_controls_match else None

# 2. CSS样式部分
css_top_controls = '''        .top-controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
'''
css_btn_secondary = '''        .btn-secondary {
            background: linear-gradient(135deg, #764ba2 0%, #6a3093 100%);
            color: white;
        }
'''

# 3. JS函数部分
speakPhrase_prefix = '''        function speakPhrase(index, type, rate) {
            // 点击卡片按钮时，先停止循环播放
            if (isLooping) {
                isLooping = false;
                loopCount = MAX_LOOPS;
                const statusEl = document.getElementById('loopStatus');
                if (statusEl) statusEl.textContent = '⏹ 已切换到单卡片模式';
            }

            const phrase = phrases[index];'''

stopSpeaking_func = '''        function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            const statusEl = document.getElementById('loopStatus');
            const btnEl = document.getElementById('loopBtn');
            if (statusEl) statusEl.textContent = '⏹ 已停止';
            if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
        }

        function goBack() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            const statusEl = document.getElementById('loopStatus');
            const btnEl = document.getElementById('loopBtn');
            if (statusEl) statusEl.textContent = '⏹ 已停止';
            if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
            window.location.href = 'index.html';
        }
'''


def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # 1. 添加top-controls到正确位置
    if top_controls:
        # 检查是否已经有top-controls
        if 'class="top-controls"' not in content:
            # 在header结束后添加
            pattern = r'(<div class="grade">.*?</div>\s*</div>\s*)'
            if re.search(pattern, content):
                content = re.sub(pattern, r'\1\n\n' + top_controls, content)
                modified = True
    
    # 2. 添加CSS样式
    if '.top-controls' not in content:
        pattern = r'(\.card \{)'
        content = re.sub(pattern, css_top_controls + r'\1', content)
        modified = True
    
    if '.btn-secondary' not in content:
        # 在.btn-loop样式后添加
        pattern = r'(\.btn-loop \{[^}]+\})'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1\n' + css_btn_secondary, content)
            modified = True
    
    # 3. 修复speakPhrase函数
    old_speakPhrase = '''        function speakPhrase(index, type, rate) {
            const phrase = phrases[index];'''
    
    if old_speakPhrase in content and '// 点击卡片按钮时' not in content:
        content = content.replace(old_speakPhrase, speakPhrase_prefix)
        modified = True
    
    # 4. 修复stopSpeaking和goBack函数
    old_stopGoBack = '''        function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = 0;
            document.getElementById('loopStatus').textContent = '⏹ 已停止';
        }
function goBack() {
    window.speechSynthesis.cancel();
    isLooping = false;
    loopCount = MAX_LOOPS;
    const statusEl = document.getElementById('loopStatus');
    const btnEl = document.getElementById('loopBtn');
    if (statusEl) statusEl.textContent = '⏹ 已停止';
    if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
    window.location.href = 'index.html';
}'''
    
    if old_stopGoBack in content:
        content = content.replace(old_stopGoBack, stopSpeaking_func)
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
