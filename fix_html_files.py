#!/usr/bin/env python3
"""批量修复HTML文件：添加循环按钮、修复汉语音频（幂等版本）"""

import os
import re
import glob

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 检查是否已经修复过（防止重复）
    if 'function toggleLoop()' in content:
        print(f"[--] Already fixed: {filepath}")
        return False
    
    # 修复1: 添加window.speechSynthesis.speak(cnUtterance);
    # 只在还没有speak(cnUtterance)的情况下添加
    
    # 修复慢速词的中文播放
    if "const cnUtterance = speak(phrase.zh" in content:
        content = re.sub(
            r"(const cnUtterance = speak\(phrase\.zh, 0\.9, 'zh-CN'\);)",
            r"\1\n                        window.speechSynthesis.speak(cnUtterance);",
            content
        )
    
    # 修复慢速句的中文播放
    if "const cnUtterance = speak(phrase.example_zh" in content:
        content = re.sub(
            r"(const cnUtterance = speak\(phrase\.example_zh, 0\.9, 'zh-CN'\);)",
            r"\1\n                        window.speechSynthesis.speak(cnUtterance);",
            content
        )
    
    # 修复2: 在loop-status之前插入循环按钮
    loop_button_html = '''
        <div class="button-group" style="justify-content: center; margin-bottom: 20px;">
            <button class="btn btn-loop" id="loopBtn" onclick="toggleLoop()">
                ▶️ 开始循环朗读
            </button>
        </div>
    '''
    
    # 只在没有loopBtn的情况下添加
    if 'id="loopBtn"' not in content:
        content = re.sub(
            r'(<div class="loop-status" id="loopStatus">)',
            loop_button_html + r'\n\n        \1',
            content
        )
    
    # 修复3: 添加toggleLoop函数，更新stopSpeaking函数
    new_stop_and_toggle = '''function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = 0;
            document.getElementById('loopStatus').textContent = '⏹ 已停止';
            document.getElementById('loopBtn').textContent = '▶️ 开始循环朗读';
        }

        function toggleLoop() {
            const btn = document.getElementById('loopBtn');
            if (isLooping) {
                window.speechSynthesis.cancel();
                isLooping = false;
                document.getElementById('loopStatus').textContent = '⏹ 已停止';
                btn.textContent = '▶️ 开始循环朗读';
            } else {
                if (loopCount === 0) {
                    loopCount = 1;
                }
                startAutoLoop();
                btn.textContent = '⏸ 暂停循环';
            }
        }'''
    
    # 只在没有toggleLoop的情况下替换
    if 'function toggleLoop()' not in content:
        content = re.sub(
            r'function stopSpeaking\(\) \{[^}]+\}',
            new_stop_and_toggle,
            content
        )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # 设置控制台编码
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 获取所有HTML文件
    html_files = glob.glob('2026-*.html') + glob.glob('2027-*.html')
    html_files.sort()
    
    fixed_count = 0
    for filepath in html_files:
        if fix_html_file(filepath):
            fixed_count += 1
            print(f"[OK] {filepath}")
        else:
            print(f"[--] {filepath}")
    
    print(f"\nTotal: Fixed {fixed_count} files")

if __name__ == '__main__':
    main()
