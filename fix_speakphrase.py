# -*- coding: utf-8 -*-
"""
修复 speakPhrase 函数，添加 fromLoop 参数区分"循环调用"和"用户点击"
只有在用户点击卡片按钮时才停止循环
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

OLD_SPREAKPHRASE = '''function speakPhrase(index, type, rate) {
            // 点击卡片按钮时，先停止循环播放
            if (isLooping) {
                isLooping = false;
                loopCount = MAX_LOOPS;
                const statusEl = document.getElementById('loopStatus');
                if (statusEl) statusEl.textContent = '⏹ 已切换到单卡片模式';
            }'''

NEW_SPREAKPHRASE = '''function speakPhrase(index, type, rate, fromLoop = false) {
            // 点击卡片按钮时，先停止循环播放
            // 只有用户手动点击卡片按钮时才停止循环，循环播放内部调用不应停止
            if (isLooping && !fromLoop) {
                isLooping = false;
                loopCount = MAX_LOOPS;
                const statusEl = document.getElementById('loopStatus');
                if (statusEl) statusEl.textContent = '⏹ 已切换到单卡片模式';
            }'''

OLD_STARTSPEAK = '''speakPhrase(i, 'word', 0.4);'''
NEW_STARTSPEAK = '''speakPhrase(i, 'word', 0.4, true);'''

count_fixed = 0
count_skipped = 0

for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue

    filepath = filename
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 检查是否已经修复（已经有了 fromLoop 参数）
    if 'fromLoop = false' in content:
        count_skipped += 1
        continue

    # 替换 speakPhrase 函数签名
    content = content.replace(
        'function speakPhrase(index, type, rate) {',
        'function speakPhrase(index, type, rate, fromLoop = false) {'
    )

    # 替换条件判断
    content = content.replace(
        '''// 点击卡片按钮时，先停止循环播放
            if (isLooping) {''',
        '''// 点击卡片按钮时，先停止循环播放
            // 只有用户手动点击卡片按钮时才停止循环，循环播放内部调用不应停止
            if (isLooping && !fromLoop) {'''
    )

    # 替换循环中的调用
    content = content.replace("speakPhrase(i, 'word', 0.4);", "speakPhrase(i, 'word', 0.4, true);")
    content = content.replace("speakPhrase(i, 'word', 0.8);", "speakPhrase(i, 'word', 0.8, true);")
    content = content.replace("speakPhrase(i, 'sentence', 0.6);", "speakPhrase(i, 'sentence', 0.6, true);")
    content = content.replace("speakPhrase(i, 'sentence', 0.8);", "speakPhrase(i, 'sentence', 0.8, true);")
    content = content.replace("speakPhrase(i, 'sentence', 0.9);", "speakPhrase(i, 'sentence', 0.9, true);")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count_fixed += 1
        print(f'Fixed: {filename}')

print(f'\nTotal: Fixed {count_fixed} files, Skipped {count_skipped} files')
