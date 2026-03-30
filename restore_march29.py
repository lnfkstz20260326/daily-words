#!/usr/bin/env python3
"""
把3月29日的完整JS语音逻辑，替换到当前版本
修正选择器匹配当前HTML的类名
"""

import os
import re
import shutil

# 3月29日的完整JS代码（修正选择器）
MARCH29_JS = '''let isPlaying=false,currentLoop=0,maxLoops=7;
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
    isPlaying=false;
    window.speechSynthesis.cancel();
    const statusDiv=document.getElementById('loopStatus');
    statusDiv.textContent='⏸ 已暂停';
    document.querySelector('.btn-primary').textContent='▶️ 继续朗读';
    return;
  }
  isPlaying=true;
  currentLoop=0;
  const statusDiv=document.getElementById('loopStatus');
  const btn=document.querySelector('.btn-primary');
  statusDiv.style.display='block';
  const cards=document.querySelectorAll('.card');
  while(isPlaying&&currentLoop<maxLoops){
    currentLoop++;
    statusDiv.textContent='🔄 第'+currentLoop+'/'+maxLoops+'轮';
    btn.textContent='⏸ 暂停';
    for(let c of cards){
      if(!isPlaying)break;
      const wordEn=c.querySelector('.word-title').textContent;
      const wordZh=c.querySelector('.chinese-meaning').textContent;
      const exEn=c.querySelector('.example-en').textContent;
      const exZh=c.querySelector('.example-cn').textContent;
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
      for(let i=0;i<3;i++){if(!isPlaying)break;await speakSentence(exEn,exZh,'fast');await new Promise(r=>setTimeout(r,600));}
      await new Promise(r=>setTimeout(r,1000));
    }
  }
  isPlaying=false;
  statusDiv.textContent='✅ 完成';
  btn.textContent='▶️ 开始循环朗读';
}
function goBack(){
  stopSpeaking();
  setTimeout(()=>location.href='index.html',100);
}
// 3秒后自动开始
setTimeout(()=>{startAutoPlay();},3000);'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换script标签中的JS代码
    old_script_pattern = r'<script>let isPlaying=false,currentLoop=0,maxLoops=7;.*?setTimeout\(\(\)=>\{startAutoPlay\(\);\},3000\);</script>'
    new_script = f'<script>{MARCH29_JS}</script>'
    
    if re.search(old_script_pattern, content, re.DOTALL):
        content = re.sub(old_script_pattern, new_script, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # 先备份当前版本
    backup_dir = './backup_before_march29_restore'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        for filename in sorted(os.listdir('.')):
            if filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename):
                shutil.copy2(filename, backup_dir)
        print(f'Backup saved to: {backup_dir}')
    
    count = 0
    for filename in sorted(os.listdir('.')):
        if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
            continue
        
        filepath = os.path.join('.', filename)
        if fix_file(filepath):
            count += 1
            print(f'Fixed: {filename}')
    
    print(f'\nTotal: {count} files fixed')
    print('March 29 JS logic applied with corrected selectors:')
    print('  .card, .word-title, .chinese-meaning, .example-en, .example-cn')

if __name__ == '__main__':
    main()
