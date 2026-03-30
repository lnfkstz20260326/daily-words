import json

# 读取素材库
with open('content_backup/content_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总共 {len(data)} 天的数据\n")

issues = []

for date, words in data.items():
    for i, word in enumerate(words):
        word_en = word.get('word_en', '').strip()
        example_en = word.get('example_en', '').strip()
        example_zh = word.get('example_zh', '').strip()
        
        # 检查问题
        problems = []
        
        # 1. 例句为空
        if not example_en or not example_zh:
            problems.append('例句为空')
        
        # 2. 例句和单词不匹配（简单检查：例句中不包含单词）
        # 注意：这是启发式检查，可能有误判
        if example_en and word_en:
            # 如果例句很短或者明显是别的词
            word_lower = word_en.lower()
            example_lower = example_en.lower()
            
            # 简单检查：例句中是否包含单词本身（忽略大小写）
            # 但要排除短语情况
            if ' ' not in word_en and word_lower not in example_lower:
                # 例句可能不包含单词
                pass  # 这个检查太严格，跳过
        
        # 3. 检查是否和前一个词的例句相同（真正的重复问题）
        if i > 0:
            prev_example = words[i-1].get('example_en', '').strip().lower()
            if prev_example and example_en:
                if example_en.lower() == prev_example:
                    problems.append(f'例句与上一个词相同')
        
        if problems:
            issues.append({
                'date': date,
                'index': i + 1,
                'word': word_en,
                'problems': problems,
                'example': example_en,
                'prev_word': words[i-1].get('word_en', '') if i > 0 else '',
                'prev_example': words[i-1].get('example_en', '') if i > 0 else ''
            })

print(f"发现 {len(issues)} 个问题\n")
print("=" * 60)

# 按问题类型分类
empty_examples = [x for x in issues if '例句为空' in x['problems']]
duplicate_examples = [x for x in issues if '例句与上一个词相同' in x['problems']]

print(f"\n[例句为空] 的问题：{len(empty_examples)} 个")
if empty_examples:
    for item in empty_examples[:20]:
        print(f"  {item['date']} 第{item['index']}个词 '{item['word']}' - 例句为空")
    if len(empty_examples) > 20:
        print(f"  ... 还有 {len(empty_examples) - 20} 个")

print(f"\n[例句与上一个词重复] 的问题：{len(duplicate_examples)} 个")
if duplicate_examples:
    for item in duplicate_examples[:20]:
        print(f"  {item['date']} 第{item['index']}个词 '{item['word']}' - 例句: '{item['example']}'")
        print(f"    上一个词 '{item['prev_word']}' 的例句: '{item['prev_example']}'")
    if len(duplicate_examples) > 20:
        print(f"  ... 还有 {len(duplicate_examples) - 20} 个")

# 统计受影响的日期
affected_dates = set([x['date'] for x in issues])
print(f"\n[受影响日期数量]：{len(affected_dates)} 天")
