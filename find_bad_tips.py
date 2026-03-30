import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('content_backup/content_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 找出所有"记住xxx的英文表达"类型的废话
bad_tips = []
useless_patterns = []

for date, words in data.items():
    for word in words:
        tip = word.get('memory_tip', '')
        if not tip:
            continue
        
        # 检查是否是废话类型
        if '记住' in tip and '英文表达' in tip:
            bad_tips.append((date, word['word_en'], tip))
        # 检查是否是简单的"xxx=xxx"拆分（不够深入）
        elif re.match(r'^记忆小提示：[\u4e00-\u9fa5]+=[\u4e00-\u9fa5]+$', tip):
            useless_patterns.append((date, word['word_en'], tip))
        # 检查是否是简单的"xxx=xxx,xxx"拆分
        elif re.match(r'^记忆小提示：[\u4e00-\u9fa5]+=[\u4e00-\u9fa5]+，[\u4e00-\u9fa5]+$', tip):
            useless_patterns.append((date, word['word_en'], tip))

print(f"【记住xxx的英文表达】类型废话: {len(bad_tips)} 个")
for d, w, t in bad_tips[:20]:
    print(f"  {d} - {w}: {t}")

print(f"\n【简单=拆分无实际帮助】提示: {len(useless_patterns)} 个")
for d, w, t in useless_patterns[:20]:
    print(f"  {d} - {w}: {t}")
