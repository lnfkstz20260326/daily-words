# -*- coding: utf-8 -*-
"""
一体化修复脚本 - 彻底修复按钮控制
"""

import glob
import re

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # =========================================
    # 修复1: 添加顶部控制按钮区域（如果不存在）
    # =========================================
    if 'class="top-controls"' not in content:
        # 在 header 结束后添加
        header_end = content.find('</div>\n\n        <div class="card">')
        if header_end != -1:
            top_controls = '''
        <div class="top-controls">
            <button class="btn btn-loop" id="loopBtn" onclick="toggleLoop()">
                ▶️ 开始循环朗读
            </button>
            <button class="btn btn-secondary" onclick="goBack()">
                ⬅️ 返回选择
            </button>
        </div>

'''
            content = content[:header_end + 6] + top_controls + content[header_end + 6:]
    
    # =========================================
    # 修复2: 添加 top-controls 样式
    # =========================================
    if '.top-controls' not in content:
        # 在 .header 样式后添加
        header_style_end = content.find('.card {')
        if header_style_end != -1:
            new_style = '''
        .top-controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
'''
            content = content[:header_style_end] + new_style + content[header_style_end:]
    
    # =========================================
    # 修复3: 添加 .btn-secondary 样式
    # =========================================
    if '.btn-secondary' not in content:
        btn_loop_end = content.find('.btn-loop {')
        if btn_loop_end != -1:
            # 找到 btn-loop 样式的结束位置
            next_brace = content.find('}', btn_loop_end)
            if next_brace != -1:
                new_style = '''
        .btn-secondary {
            background: linear-gradient(135deg, #764ba2 0%, #6a3093 100%);
            color: white;
        }
'''
                content = content[:next_brace + 1] + new_style + content[next_brace + 1:]
    
    # =========================================
    # 修复4: 修复 speakPhrase 函数 - 添加循环停止逻辑
    # =========================================
    old_speakPhrase = '''function speakPhrase(index, type, rate) {
            const phrase = phrases[index];
            let text, lang;

            if (type === 'word') {
                text = phrase.en;
                lang = 'en-US';
            } else {
                text = phrase.example;
                lang = 'en-US';
            }

            window.speechSynthesis.cancel();'''

    new_speakPhrase = '''function speakPhrase(index, type, rate) {
            // 点击卡片按钮时，先停止循环播放
            if (isLooping) {
                isLooping = false;
                loopCount = MAX_LOOPS;
                const statusEl = document.getElementById('loopStatus');
                if (statusEl) statusEl.textContent = '⏹ 已切换到单卡片模式';
            }

            const phrase = phrases[index];
            let text, lang;

            if (type === 'word') {
                text = phrase.en;
                lang = 'en-US';
            } else {
                text = phrase.example;
                lang = 'en-US';
            }

            window.speechSynthesis.cancel();'''

    if old_speakPhrase in content:
        content = content.replace(old_speakPhrase, new_speakPhrase)
    
    # =========================================
    # 修复5: 修复 stopSpeaking 函数
    # =========================================
    if 'function stopSpeaking()' in content:
        old_stop = '''function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = 0;
            document.getElementById('loopStatus').textContent = '⏹ 已停止';
            document.getElementById('loopBtn').textContent = '▶️ 开始循环朗读';
        }'''

        new_stop = '''function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            const statusEl = document.getElementById('loopStatus');
            const btnEl = document.getElementById('loopBtn');
            if (statusEl) statusEl.textContent = '⏹ 已停止';
            if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
        }'''

        if old_stop in content and new_stop not in content:
            content = content.replace(old_stop, new_stop)
    
    # =========================================
    # 修复6: 添加 goBack 函数
    # =========================================
    if 'function goBack()' not in content and 'function stopSpeaking()' in content:
        goback_func = '''
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
        # 在 stopSpeaking 后添加
        stop_end = content.find('function stopSpeaking()')
        if stop_end != -1:
            # 找到 stopSpeaking 函数的结束 }
            brace_count = 0
            started = False
            for i in range(stop_end, len(content)):
                if content[i] == '{':
                    brace_count += 1
                    started = True
                elif content[i] == '}':
                    brace_count -= 1
                    if started and brace_count == 0:
                        insert_pos = i + 1
                        content = content[:insert_pos] + goback_func + content[insert_pos:]
                        break
    
    # =========================================
    # 修复7: 修复 toggleLoop 函数中的按钮文字
    # =========================================
    if "btn.textContent = '⏸ 暂停循环'" in content:
        # 确保 toggleLoop 函数正确
        old_toggle = "btn.textContent = '⏸ 暂停循环';"
        new_toggle = "btn.textContent = '⏸ 暂停';"
        if old_toggle in content:
            content = content.replace(old_toggle, new_toggle)
    
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
