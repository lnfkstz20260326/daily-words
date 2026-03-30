#!/usr/bin/env python3
"""修复语音播放：改进voice selection + 确保汉语正常播放"""

import os
import re

# 完整的新JS代码模板 - 基于3月29日但改进voice selection
NEW_JS_TEMPLATE = '''let isPlaying=false,currentLoop=0,maxLoops=7;
// 优化后的loadVoices函数
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
// 改进的voice selection - 优先选择高质量语音
function selectVoice(voices, lang) {
  // 英文高质量语音优先级
  if(lang === 'en-US') {
    const preferred = ['Jenny', 'Aria', 'Samantha', 'Microsoft Aria', 'Google US English', 'Microsoft David'];
    for(const name of preferred) {
      const v = voices.find(v => v.name.includes(name) && v.lang.startsWith('en'));
      if(v) return v;
    }
    // 回退到任何英文语音
    const enVoice = voices.find(v => v.lang.startsWith('en'));
    return enVoice || voices[0];
  }
  // 中文语音选择
  if(lang === 'zh-CN') {
    const preferred = ['Huihui', 'Yaoyao', 'Kangkang', 'Wang', 'Microsoft Huihui'];
    for(const name of preferred) {
      const v = voices.find(v => v.name.includes(name) && v.lang.startsWith('zh'));
      if(v) return v;
    }
    // 回退到任何中文语音
    const zhVoice = voices.find(v => v.lang.startsWith('zh'));
    return zhVoice || voices[0];
  }
  return voices[0];
}
// speakWord: 播放单词
async function speakWord(wordEn,wordZh,speed){
  window.speechSynthesis.cancel();
  const voices=await loadVoices();
  const voice=selectVoice(voices,'en-US');
  let rate=speed==='slow'?0.4:0.8;
  for(let i=0;i<3;i++){
    const u=new SpeechSynthesisUtterance(wordEn);
    u.lang='en-US';u.rate=rate;u.voice=voice;
    window.speechSynthesis.speak(u);
    await new Promise(r=>setTimeout(r,500));
  }
  if(speed==='slow'){
    setTimeout(()=>{
      const cnVoice=selectVoice(voices,'zh-CN');
      const u2=new SpeechSynthesisUtterance(wordZh);
      u2.lang='zh-CN';u2.rate=1.0;u2.voice=cnVoice;
      window.speechSynthesis.speak(u2);
    },1500);
  }
}
// speakSentence: 播放句子
async function speakSentence(exEn,exZh,speed){
  window.speechSynthesis.cancel();
  const voices=await loadVoices();
  const voice=selectVoice(voices,'en-US');
  let rate=speed==='slow'?0.6:speed==='fast'?0.9:0.8;
  for(let i=0;i<3;i++){
    const u=new SpeechSynthesisUtterance(exEn);
    u.lang='en-US';u.rate=rate;u.voice=voice;
    window.speechSynthesis.speak(u);
    await new Promise(r=>setTimeout(r,600));
  }
  if(speed==='slow'){
    setTimeout(()=>{
      const cnVoice=selectVoice(voices,'zh-CN');
      const u2=new SpeechSynthesisUtterance(exZh);
      u2.lang='zh-CN';u2.rate=1.0;u2.voice=cnVoice;
      window.speechSynthesis.speak(u2);
    },2000);
  }
}
// speakPhrase: 卡片按钮调用的桥接函数
async function speakPhrase(index, type, rate){
  const card=document.querySelectorAll('.card')[index];
  if(!card)return;
  const wordEn=card.querySelector('.word-title').textContent;
  const wordZh=card.querySelector('.chinese-meaning').textContent;
  const exEn=card.querySelector('.example-en').textContent;
  const exZh=card.querySelector('.example-cn').textContent;
  const speed=rate<=0.6?'slow':rate<=0.7?'normal':'fast';
  if(type==='word'){
    await speakWord(wordEn,wordZh,speed);
  }else{
    await speakSentence(exEn,exZh,speed);
  }
}
function stopSpeaking(){
  window.speechSynthesis.cancel();
  isPlaying=false;
  currentLoop=0;
  const statusDiv=document.getElementById('loopStatus');
  statusDiv.style.display='block';
  statusDiv.textContent='⏹ 已停止';
  document.querySelector('.btn-loop').textContent='▶️ 开始循环朗读';
}
async function startAutoPlay(){
  if(isPlaying)return;
  isPlaying=true;
  currentLoop=0;
  const statusDiv=document.getElementById('loopStatus');
  const btn=document.querySelector('.btn-loop');
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
    new_script = f'<script>{NEW_JS_TEMPLATE}</script>'
    
    if re.search(old_script_pattern, content, re.DOTALL):
        content = re.sub(old_script_pattern, new_script, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    count = 0
    for filename in sorted(os.listdir('.')):
        if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
            continue
        
        filepath = os.path.join('.', filename)
        if fix_file(filepath):
            count += 1
            print(f'Fixed: {filename}')
    
    print(f'\nTotal: {count} files fixed')

if __name__ == '__main__':
    main()
