# -*- coding: utf-8 -*-
"""
恢复到3月29日稳定版本的JS逻辑
使用3月29日的模板替换所有文件的JS部分
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 3月29日稳定版的JS模板
STABLE_JS = '''<script>
let isPlaying=false,currentLoop=0,maxLoops=7;
function loadVoices(){
  return new Promise(resolve=>{
    let voices=window.speechSynthesis.getVoices();
    if(voices.length>0){
      resolve(voices);
    }else{
      window.speechSynthesis.onvoiceschanged=()=>{
        voices=window.speechSynthesis.getVoices();
        resolve(voices);
      };
    }
  });
}
async function speakWord(wordEn,wordZh,speed){
  window.speechSynthesis.cancel();
  const voices=await loadVoices();
  let rate=speed==='slow'?0.4:0.8;
  for(let i=0;i<3;i++){
    const u=new SpeechSynthesisUtterance(wordEn);
    u.lang='en-US';u.rate=rate;
    const v=voices.find(v=>v.name.includes('Jenny'))||voices.find(v=>v.name.includes('Aria'))||voices.find(v=>v.name.includes('Google US English'))||voices[0];
    if(v)u.voice=v;
    window.speechSynthesis.speak(u);
    await new Promise(r=>setTimeout(r,500));
  }
  if(speed==='slow'){
    setTimeout(()=>{
      const u2=new SpeechSynthesisUtterance(wordZh);
      u2.lang='zh-CN';u2.rate=1.0;
      window.speechSynthesis.speak(u2);
    },1500);
  }
}
async function speakSentence(exEn,exZh,speed){
  window.speechSynthesis.cancel();
  const voices=await loadVoices();
  let rate=speed==='slow'?0.6:speed==='fast'?0.9:0.8;
  for(let i=0;i<3;i++){
    const u=new SpeechSynthesisUtterance(exEn);
    u.lang='en-US';u.rate=rate;
    const v=voices.find(v=>v.name.includes('Jenny'))||voices.find(v=>v.name.includes('Aria'))||voices.find(v=>v.name.includes('Google US English'))||voices[0];
    if(v)u.voice=v;
    window.speechSynthesis.speak(u);
    await new Promise(r=>setTimeout(r,600));
  }
  if(speed==='slow'){
    setTimeout(()=>{
      const u2=new SpeechSynthesisUtterance(exZh);
      u2.lang='zh-CN';u2.rate=1.0;
      window.speechSynthesis.speak(u2);
    },2000);
  }
}
function stopSpeaking(){
  window.speechSynthesis.cancel();
  isPlaying=false;
  currentLoop=0;
  const statusDiv=document.getElementById('loopStatus');
  statusDiv.style.display='block';
  statusDiv.textContent='⏹ 已停止';
  document.querySelector('.btn-primary').textContent='▶️ 开始循环朗读';
}
async function startAutoPlay(){
  if(isPlaying){
    // 正在播放 -> 暂停
    isPlaying=false;
    currentLoop=0;
    window.speechSynthesis.cancel();
    const statusDiv=document.getElementById('loopStatus');
    statusDiv.textContent='⏸ 已暂停';
    document.querySelector('.btn-primary').textContent='▶️ 继续朗读';
    return;
  }
  // 开始播放
  isPlaying=true;
  currentLoop=0;
  const statusDiv=document.getElementById('loopStatus');
  const btn=document.querySelector('.btn-primary');
  statusDiv.style.display='block';
  const cards=document.querySelectorAll('.word-card');
  while(isPlaying&&currentLoop<maxLoops){
    currentLoop++;
    statusDiv.textContent='🔄 第'+currentLoop+'/'+maxLoops+'轮';
    btn.textContent='⏸ 暂停循环';
    for(let c of cards){
      if(!isPlaying)break;
      const wordEn=c.querySelector('.word-en').textContent;
      const wordZh=c.querySelector('.word-meaning').textContent;
      const exEn=c.querySelector('.example-en').textContent;
      const exZh=c.querySelector('.example-zh').textContent;
      // 1. 慢速词×3 + 汉语
      for(let i=0;i<3;i++){if(!isPlaying)break;await speakWord(wordEn,wordZh,'slow');await new Promise(r=>setTimeout(r,500));}
      if(isPlaying){await new Promise(r=>setTimeout(r,500));}
      // 2. 匀速词×3（不加汉语）
      for(let i=0;i<3;i++){if(!isPlaying)break;await speakWord(wordEn,wordZh,'normal');await new Promise(r=>setTimeout(r,500));}
      await new Promise(r=>setTimeout(r,500));
      // 3. 慢速句×3 + 汉语
      for(let i=0;i<3;i++){if(!isPlaying)break;await speakSentence(exEn,exZh,'slow');await new Promise(r=>setTimeout(r,600));}
      if(isPlaying){await new Promise(r=>setTimeout(r,500));}
      // 4. 匀速句×3（不加汉语）
      for(let i=0;i<3;i++){if(!isPlaying)break;await speakSentence(exEn,exZh,'normal');await new Promise(r=>setTimeout(r,600));}
      await new Promise(r=>setTimeout(r,500));
      // 5. 常速句×3（不加汉语）
      for(let i=0;i<3;i++){if(!isPlaying)break;await speakSentence(exEn,exZh,'fast');await new Promise(r=>setTimeout(r,500));}
      await new Promise(r=>setTimeout(r,1000));
    }
    if(currentLoop>=maxLoops){
      isPlaying=false;
      statusDiv.textContent='✅ 已完成'+maxLoops+'轮';
      btn.textContent='▶️ 开始循环朗读';
    }
  }
}
function goBack(){
  window.speechSynthesis.cancel();
  isPlaying=false;
  currentLoop=0;
  setTimeout(()=>{window.location.href='index.html';},100);
}
// 页面加载3秒后自动开始循环朗读
setTimeout(()=>{startAutoPlay();},3000);
'''

def extract_card_buttons(html_content):
    """从HTML中提取每个卡片的中英文内容"""
    cards = []
    card_pattern = r'<div class="word-card">(.*?)</div>\s*(?=<div class="word-card">|</body>)'
    word_en_pattern = r'<div class="word-en">([^<]+)</div>'
    word_zh_pattern = r'<div class="word-meaning">([^<]+)</div>'
    example_en_pattern = r'<div class="example-en">([^<]+)</div>'
    example_zh_pattern = r'<div class="example-zh">([^<]+)</div>'
    
    # 提取所有卡片
    for card_match in re.finditer(card_pattern, html_content, re.DOTALL):
        card_html = card_match.group(1)
        
        word_en = re.search(word_en_pattern, card_html)
        word_zh = re.search(word_zh_pattern, card_html)
        ex_en = re.search(example_en_pattern, card_html)
        ex_zh = re.search(example_zh_pattern, card_html)
        
        if word_en:
            word_en_text = word_en.group(1).strip()
            word_zh_text = word_zh.group(1).strip() if word_zh else ''
            ex_en_text = ex_en.group(1).strip() if ex_en else ''
            ex_zh_text = ex_zh.group(1).strip() if ex_zh else ''
            
            # 按钮HTML
            buttons = f'''  <div class="controls">
    <button class="btn btn-slow" onclick="speakWord('{word_en_text}','{word_zh_text}','slow')">🐢 慢速词×3</button>
    <button class="btn btn-normal" onclick="speakWord('{word_en_text}','{word_zh_text}','normal')">🚀 匀速词×3</button>
    <button class="btn btn-slow" onclick="speakSentence('{ex_en_text}','{ex_zh_text}','slow')">🐢 慢速句×3</button>
    <button class="btn btn-normal" onclick="speakSentence('{ex_en_text}','{ex_zh_text}','normal')">🚀 匀速句×3</button>
    <button class="btn btn-fast" onclick="speakSentence('{ex_en_text}','{ex_zh_text}','fast')">⚡ 常速句×3</button>
    <button class="btn btn-stop" onclick="stopSpeaking()">⏹ 停止</button>
  </div>'''
            cards.append(buttons)
    
    return cards

def fix_file(filepath):
    """修复单个HTML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经包含稳定版的JS
    if 'let isPlaying=false,currentLoop=0' in content:
        return False, 'already stable'
    
    # 提取卡片按钮
    cards = extract_card_buttons(content)
    if not cards:
        return False, 'no cards found'
    
    # 提取日期和标题信息
    date_pattern = r'<div class="date-info">([^<]+)</div>'
    date_match = re.search(date_pattern, content)
    date_info = date_match.group(1) if date_match else ''
    
    # 提取标题
    title_pattern = r'<title>([^<]+)</title>'
    title_match = re.search(title_pattern, content)
    title = title_match.group(1) if title_match else '每日英语听说'
    
    # 构建顶部控制区
    top_controls = '''  <div class="top-controls">
    <button class="btn btn-primary" onclick="startAutoPlay()">▶️ 开始循环朗读</button>
    <button class="btn btn-secondary" onclick="goBack()">⬅️ 返回首页</button>
  </div>'''
    
    # 查找并替换top-controls
    top_controls_pattern = r'<div class="top-controls">.*?</div>'
    if re.search(top_controls_pattern, content, re.DOTALL):
        content = re.sub(top_controls_pattern, top_controls, content, flags=re.DOTALL)
    
    # 替换所有卡片的controls部分
    card_pattern = r'(<div class="word-card">.*?<div class="word-tip">.*?</div>\s*)(<div class="controls">.*?</div>)'
    
    def replace_card(match):
        prefix = match.group(1)
        return prefix
    
    # 使用更简单的方法：找到每个controls div并替换
    controls_pattern = r'<div class="controls">.*?</div>\s*(?=</div>\s*$|</script>)'
    
    for i, card_buttons in enumerate(cards):
        if i == 0:
            # 第一个卡片
            content = re.sub(controls_pattern, card_buttons + '\n', content, count=1, flags=re.DOTALL)
        else:
            # 后续卡片
            content = re.sub(controls_pattern, card_buttons + '\n', content, count=1, flags=re.DOTALL)
    
    # 替换script标签内容
    script_pattern = r'<script>[\s\S]*?</script>'
    content = re.sub(script_pattern, STABLE_JS + '\n</script>', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, 'fixed'

def main():
    count_fixed = 0
    count_skipped = 0
    count_error = 0
    
    for filename in sorted(os.listdir('.')):
        if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
            continue
        
        try:
            success, reason = fix_file(filename)
            if success:
                count_fixed += 1
                print(f'Fixed: {filename}')
            else:
                count_skipped += 1
                if 'already' not in reason:
                    print(f'Skipped: {filename} ({reason})')
        except Exception as e:
            count_error += 1
            print(f'Error: {filename} - {e}')
    
    print(f'\nTotal: Fixed {count_fixed}, Skipped {count_skipped}, Errors {count_error}')

if __name__ == '__main__':
    main()
