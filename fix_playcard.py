import os

old_code = """// ========== 卡片按钮播放 ==========
async function playCard(cardIndex, type, speed) {
    const cards = document.querySelectorAll('.card');"""

new_code = """// ========== 卡片按钮播放 ==========
async function playCard(cardIndex, type, speed) {
    // 设置播放状态，允许中途停止
    isPlaying = true;
    
    const cards = document.querySelectorAll('.card');"""

count = 0
for filename in os.listdir('.'):
    if filename.endswith('.html') and filename != 'index.html':
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_code in content:
                new_content = content.replace(old_code, new_code)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f'Fixed: {filename}')
        except Exception as e:
            print(f'Error {filename}: {e}')

print(f'\nTotal fixed: {count} files')
