# 内容提取脚本 - 从HTML提取英文内容和记忆提示
import os
import re
import json

all_content = {}

for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    filepath = os.path.join('.', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    date = filename.replace('.html', '')
    cards = []
    
    # 分割每个卡片
    card_blocks = re.split(r'<div class="card">', content)
    
    for block in card_blocks[1:]:  # 跳过第一个空块
        # 提取英文单词
        word_en = re.search(r'<span class="word-title">([^<]+)</span>', block)
        word_en = word_en.group(1).strip() if word_en else ''
        
        # 提取音标
        phonetic = re.search(r'<span class="phonetic">([^<]+)</span>', block)
        phonetic = phonetic.group(1).strip() if phonetic else ''
        
        # 提取词性
        pos = re.search(r'<span class="part-of-speech">([^<]+)</span>', block)
        pos = pos.group(1).strip() if pos else ''
        
        # 提取中文意思
        word_zh = re.search(r'<span class="chinese-meaning">([^<]+)</span>', block)
        word_zh = word_zh.group(1).strip() if word_zh else ''
        
        # 提取例句英文
        example_en = re.search(r'<div class="example-en">([^<]+)</div>', block)
        example_en = example_en.group(1).strip() if example_en else ''
        
        # 提取例句中文
        example_zh = re.search(r'<div class="example-cn">([^<]+)</div>', block)
        example_zh = example_zh.group(1).strip() if example_zh else ''
        
        # 提取记忆提示
        memory = re.search(r'<div class="memory-tip">([^<]+(?:<[^>]*>[^<]*</[^>]*>)*[^<]*)</div>', block, re.DOTALL)
        if memory:
            memory_tip = re.sub(r'<[^>]+>', '', memory.group(0))
            memory_tip = memory_tip.strip()
            # 去掉emoji前缀
            memory_tip = re.sub(r'^[\U0001F300-\U0001F9FF]', '', memory_tip).strip()
        else:
            memory_tip = ''
        
        if word_en:
            cards.append({
                'word_en': word_en,
                'phonetic': phonetic,
                'pos': pos,
                'word_zh': word_zh,
                'example_en': example_en,
                'example_zh': example_zh,
                'memory_tip': memory_tip
            })
    
    if cards:
        all_content[date] = cards
        print(f'Extracted: {date} - {len(cards)} cards')

# 保存为JSON
os.makedirs('content_backup', exist_ok=True)
output_file = 'content_backup/content_backup.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_content, f, ensure_ascii=False, indent=2)

# 统计
total_cards = sum(len(v) for v in all_content.values())
print(f'\nTotal: {len(all_content)} dates, {total_cards} cards')
print(f'Saved to {output_file}')
