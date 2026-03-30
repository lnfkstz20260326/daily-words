"""
从3月29日版本提取JS逻辑，结合正确的CSS选择器，批量应用到所有HTML文件
"""
import os
import re

# 3月29日的JS逻辑（修复版：使用正确选择器、maxLoops=7、添加speakPhrase、修复goBack）
JS_TEMPLATE = '''
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
async function startAutoPlay(){
  if(isPlaying)return;
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
  window.location.href='index.html';
}
// 页面加载3秒后自动开始循环朗读
setTimeout(()=>{startAutoPlay();},3000);
'''

def apply_js_template(filepath):
    """将新的JS模板应用到HTML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否是日期页面
    if not re.match(r'^\d{4}-\d{2}-\d{2}\.html$', os.path.basename(filepath)):
        return False
    
    # 替换script标签内容
    pattern = r'<script>[\s\S]*?</script>'
    new_script = f'<script>{JS_TEMPLATE.strip()}</script>'
    new_content = re.sub(pattern, new_script, content)
    
    if new_content == content:
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    count = 0
    for filename in sorted(os.listdir('.')):
        if not (filename.endswith('.html') and re.match(r'^\d{4}-\d{2}-\d{2}\.html$', filename)):
            continue
        
        if apply_js_template(filename):
            count += 1
            print(f'Applied: {filename}')
    
    print(f'\nTotal: {count} files updated')

if __name__ == '__main__':
    main()
