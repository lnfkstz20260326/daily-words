import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('content_backup/content_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查2026-04-01的数据
words = data.get('2026-04-01', [])
print('2026-04-01 单词记忆小提示:')
for w in words:
    tip = w['memory_tip']
    if tip:
        display = tip[:60]
    else:
        display = '(empty)'
    print(f'  {w["word_en"]:15} | {display}')

# 检查是否还有废话
print('\n检查是否还有"记住xxx的英文表达"类型的废话:')
count = 0
for date, words in data.items():
    for w in words:
        tip = w.get('memory_tip', '')
        if '记住' in tip and '英文表达' in tip:
            count += 1
            if count <= 5:
                print(f'  {date} - {w["word_en"]}: {tip}')

if count == 0:
    print('  已全部清理完毕！')
else:
    print(f'  还有 {count} 个废话')
