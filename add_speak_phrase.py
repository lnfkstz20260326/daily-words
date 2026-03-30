import os
import re

count = 0
fixed = 0

for filename in sorted(os.listdir('.')):
    if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
        continue
    
    filepath = os.path.join('.', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否缺少 speakPhrase 函数
    if 'function speakPhrase' not in content and 'speakPhrase(' in content:
        # 在 stopSpeaking 和 startAutoPlay 之间添加 speakPhrase 函数
        old_str = '''}
function stopSpeaking(){'''
        new_str = '''}
function speakPhrase(index, type, rate){
  const cards=document.querySelectorAll('.card');
  const card=cards[index];
  if(!card)return;
  const wordEn=card.querySelector('.word-title').textContent;
  const wordZh=card.querySelector('.chinese-meaning').textContent;
  const exEn=card.querySelector('.example-en').textContent;
  const exZh=card.querySelector('.example-cn').textContent;
  const speed=rate<=0.6?'slow':rate>=0.9?'fast':'normal';
  if(type==='word'){
    speakWord(wordEn,wordZh,speed);
  }else{
    speakSentence(exEn,exZh,speed);
  }
}
function stopSpeaking(){'''
        
        if old_str in content:
            content = content.replace(old_str, new_str)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f'Added speakPhrase: {filename}')
        else:
            fixed += 1
            print(f'Pattern not match: {filename}')

print(f'\nTotal: {count} files fixed, {fixed} skipped')
