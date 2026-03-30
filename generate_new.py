# 新生成器 - 使用content_backup内容生成HTML
import json
import os
from datetime import datetime, timedelta

# 读取内容备份
with open('content_backup/content_backup.json', 'r', encoding='utf-8') as f:
    content_data = json.load(f)

# 读取模板
with open('template_new.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 生成单个HTML页面
def generate_html(date_str, cards):
    # 生成卡片HTML
    cards_html = ''
    for i, card in enumerate(cards):
        card_html = f'''
    <div class="card">
        <div class="word-header">
            <div class="word-number">{i+1:02d}</div>
            <div class="word-title">{card['word_en']}</div>
            <span class="phonetic">{card['phonetic']}</span>
        </div>
        <div class="word-meaning">
            <span class="part-of-speech">{card['pos']}</span>
            <span class="chinese-meaning">{card['word_zh']}</span>
        </div>
        <div class="memory-tip">💡 {card['memory_tip']}</div>
        <div class="example-box">
            <div class="example-label">例句 Example</div>
            <div class="example-en">{card['example_en']}</div>
            <div class="example-cn">{card['example_zh']}</div>
        </div>
        <div class="button-group">
            <button class="btn btn-slow" onclick="playCard({i}, 'word', 'slow')">🐢 慢速词×3</button>
            <button class="btn btn-normal" onclick="playCard({i}, 'word', 'normal')">🚀 匀速词×3</button>
            <button class="btn btn-slow" onclick="playCard({i}, 'sentence', 'slow')">🐢 慢速句×3</button>
            <button class="btn btn-normal" onclick="playCard({i}, 'sentence', 'normal')">🚀 匀速句×3</button>
            <button class="btn btn-fast" onclick="playCard({i}, 'sentence', 'fast')">⚡ 常速句×3</button>
            <button class="btn btn-stop" onclick="stopSpeaking()">⏹ 停止</button>
        </div>
    </div>'''
        cards_html += card_html
    
    # 替换模板内容
    html = template.replace('{date}', date_str)
    html = html.replace('{cards}', cards_html)
    
    return html

# 生成所有页面
count = 0
for date_str, cards in sorted(content_data.items()):
    html = generate_html(date_str, cards)
    
    # 保存到HTML文件夹
    output_dir = 'html_output'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'{date_str}.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    count += 1
    print(f'Generated: {date_str} - {len(cards)} cards')

print(f'\nTotal: {count} files generated in {output_dir}/')
