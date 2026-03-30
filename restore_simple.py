# -*- coding: utf-8 -*-
"""
使用3月29日的稳定JS逻辑批量修复所有HTML文件
只替换JS部分，不改变HTML结构
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
</script>'''

def fix_file(filepath):
    """修复单个HTML文件 - 只替换script标签内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换script标签内容（从<script>到</script>）
    script_pattern = r'<script>[\s\S]*?</script>'
    new_content = re.sub(script_pattern, STABLE_JS, content)
    
    if new_content == content:
        return False, 'no change'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, 'fixed'

def main():
    count_fixed = 0
    count_skipped = 0
    
    for filename in sorted(os.listdir('.')):
        if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
            continue
        
        try:
            success, reason = fix_file(filename)
            if success:
                count_fixed += 1
                if count_fixed <= 10 or count_fixed % 50 == 0:
                    print(f'Fixed: {filename}')
            else:
                count_skipped += 1
        except Exception as e:
            print(f'Error: {filename} - {e}')
            count_skipped += 1
    
    print(f'\nTotal: Fixed {count_fixed}, Skipped {count_skipped}')

if __name__ == '__main__':
    main()
