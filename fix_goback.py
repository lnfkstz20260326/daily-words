#!/usr/bin/env python3
"""
修复 goBack() 函数 - 在跳转前确保音频停止
"""
import os
import re

# 旧代码模式
old_pattern = r'''function goBack\(\) \{
[^}]*window\.speechSynthesis\.cancel\(\);
[^}]*isLooping = false;
[^}]*loopCount = MAX_LOOPS;
[^}]*const statusEl = document\.getElementById\('loopStatus'\);
[^}]*const btnEl = document\.getElementById\('loopBtn'\);
[^}]*if \(statusEl\) statusEl\.textContent = '⏹ 已停止';
[^}]*if \(btnEl\) btnEl\.textContent = '▶️ 开始循环朗读';
[^}]*window\.location\.href = 'index\.html';
\}'''

# 新代码
new_code = '''function goBack() {
            // 先停止所有语音播放
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;

            // 等待音频真正停止后再跳转
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 100);
        }'''

# 匹配所有HTML文件
count = 0
fixed_count = 0

for filename in os.listdir('.'):
    if filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename):
        count += 1
        filepath = os.path.join('.', filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否需要修复
        if "setTimeout(() => {" not in content and "function goBack()" in content:
            # 使用正则替换
            new_content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f"Fixed: {filename}")

print(f"\nTotal files checked: {count}")
print(f"Files fixed: {fixed_count}")
