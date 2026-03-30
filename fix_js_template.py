import re
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

def fix_template_strings(content):
    """将模板字符串改为字符串拼接"""
    # 替换: statusDiv.textContent = `🔄 第 {currentLoop}/{maxLoops} 轮`;
    # 为:   statusDiv.textContent = '🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮';
    
    # 替换循环中的显示
    pattern1 = r"statusDiv\.textContent\s*=\s*`🔄\s*第\s*\{currentLoop\}/\{maxLoops\}\s*轮`;"
    replacement1 = "statusDiv.textContent = '🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮';"
    content = re.sub(pattern1, replacement1, content)
    
    # 替换完成消息
    pattern2 = r"statusDiv\.textContent\s*=\s*`✅\s*完成`;"
    replacement2 = "statusDiv.textContent = '✅ 完成';"
    content = re.sub(pattern2, replacement2, content)
    
    # 替换完成N轮消息
    pattern3 = r"statusDiv\.textContent\s*=\s*`✓\s*已完成\{maxLoops\}轮循环`;"
    replacement3 = "statusDiv.textContent = '✓ 已完成' + maxLoops + '轮循环';"
    content = re.sub(pattern3, replacement3, content)
    
    # 替换"已完成"按钮文字
    pattern4 = r"btn\.textContent\s*=\s*`▶️\s*开始循环朗读`;"
    replacement4 = "btn.textContent = '▶️ 开始循环朗读';"
    content = re.sub(pattern4, replacement4, content)
    
    return content

# 处理所有HTML文件
fixed_count = 0
for f in sorted(glob.glob('2026-*.html')):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = fix_template_strings(content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        fixed_count += 1

print(f"已修复 {fixed_count} 个文件")
