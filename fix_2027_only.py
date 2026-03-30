import glob

# 只修复2027年的文件
count = 0
for f in sorted(glob.glob('2027-*.html')):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '`🔄 第 {currentLoop}/{maxLoops} 轮`' in content or '`?? 第 {currentLoop}/{maxLoops} 轮`' in content:
        content = content.replace('`🔄 第 {currentLoop}/{maxLoops} 轮`', "'🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮'")
        content = content.replace('`?? 第 {currentLoop}/{maxLoops} 轮`', "'🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮'")
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1

print(f"2027年文件修复完成: {count} 个")
