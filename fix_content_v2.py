import json

# 读取素材库
with open('content_backup/content_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("开始智能修复素材库...")
print("=" * 60)

# 统计
removed_count = 0
fixed_count = 0

for date, words in data.items():
    if len(words) <= 5:
        continue  # 正常的5个词不需要处理

    new_words = []
    seen_words = {}  # 记录每个词的出现位置

    for i, word in enumerate(words):
        word_en = word.get('word_en', '').strip().lower()
        example_en = word.get('example_en', '').strip()
        example_zh = word.get('example_zh', '').strip()

        # 如果这个词已经在new_words中存在
        if word_en in seen_words:
            # 检查当前记录的例句是否正确（即例句中包含这个词）
            if example_en and word_en in example_en.lower():
                # 当前记录的例句正确，删除之前的那条
                prev_idx = seen_words[word_en]
                # 标记为需要删除
                new_words[prev_idx] = None
                seen_words[word_en] = len(new_words)
                new_words.append(word)
                fixed_count += 1
            else:
                # 当前记录的例句不正确，保留之前的
                pass  # 跳过当前记录
        else:
            seen_words[word_en] = len(new_words)
            new_words.append(word)

    # 移除被标记为删除的记录
    new_words = [w for w in new_words if w is not None]

    if len(new_words) != len(words):
        print(f"{date}: {len(words)} -> {len(new_words)} 词")

    data[date] = new_words

print(f"\n修复完成！删除了 {fixed_count} 个重复词条")

# 保存修复后的素材库
with open('content_backup/content_backup_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("已保存到 content_backup_fixed.json")

# 验证2026-04-29
words = data.get('2026-04-29', [])
print(f"\n2026-04-29 修复后有 {len(words)} 个词:")
for i, w in enumerate(words):
    print(f"  {i+1}. {w['word_en']} - 例句: '{w['example_en']}'")
