# -*- coding: utf-8 -*-
"""修复剩余的记忆提示"""
import glob

REPLACEMENTS = {
    "记住'thorsty'的英文表达": "thirsty：口渴，thirst=渴-y=...的",
    "记住'ping-pong'的英文表达": "ping-pong：乒乓球，ping-pong=拟声词",
    "记住'group work'的英文表达": "group work：小组合作，group=组work=工作",
    "记住'academic'的英文表达": "academic：学术，academ=学院ic=...的",
    "记住'vocabulary'的英文表达": "vocabulary：词汇，vocab=词ulary=表",
    "记住'grammar'的英文表达": "grammar：语法，gram=写mar=规则",
    "记住'analysis'的英文表达": "analysis：分析，an=分析alysis=拆解",
    "记住'settled'的英文表达": "settled：定居，settle=定居ed=...的",
    "记住'convenience'的英文表达": "convenience：方便，con=共同ven=来ience=便利",
    "记住chef's special": "chef's special：招牌菜，chef=厨师special=特色",
}

files = glob.glob('2026-*.html') + glob.glob('2027-*.html')
files.sort()

count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    orig = content
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
    if content != orig:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"[OK] {f}")
        count += 1
    else:
        print(f"[--] {f}")

print(f"\nFixed {count} files")
