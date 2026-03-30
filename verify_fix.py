import re

with open('2026-04-29.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取单词和例句
words = re.findall(r'<div class="word-title">(.*?)</div>', content)
examples = re.findall(r'<div class="example-en">(.*?)</div>', content)

print('2026-04-29 验证结果：')
print('=' * 40)
for i, (word, example) in enumerate(zip(words, examples)):
    print(f"{i+1}. {word:10} | 例句: {example}")

print('\n预期结果：')
print('1. fly        | 例句: Birds can fly.')
print('2. throw      | 例句: Throw the ball.')
print('3. catch      | 例句: Catch the ball!')
print('4. kick       | 例句: Kick the ball.')
print('5. hit        | 例句: Hit the ball.')
