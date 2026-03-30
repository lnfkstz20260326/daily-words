import glob
import re

# 只修复模板字符串语法这一行
count = 0
for f in glob.glob('2026-*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 只修复这一行
    if '`🔄 第 {currentLoop}/{maxLoops} 轮`' in content or '`?? 第 {currentLoop}/{maxLoops} 轮`' in content:
        content = content.replace('`🔄 第 {currentLoop}/{maxLoops} 轮`', "'🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮'")
        content = content.replace('`?? 第 {currentLoop}/{maxLoops} 轮`', "'🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮'")
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1

print(f"修复完成: {count} 个文件")
