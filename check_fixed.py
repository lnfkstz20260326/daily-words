import json

# 检查修复后的文件
with open('content_backup/content_backup_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查2026-04-29的数据
words = data.get('2026-04-29', [])
print(f'2026-04-29 修复后有 {len(words)} 个词:')
for i, w in enumerate(words):
    print(f"  {i+1}. {w['word_en']} - 例句: '{w['example_en']}'")
