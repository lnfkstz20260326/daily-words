import datetime
import json
import os
import re

def get_day_info():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    weekday = now.weekday()
    day_names = ["周一","周二","周三","周四","周五","周六","周日"]
    day_type = "word" if weekday < 5 else "phrase"
    return now.strftime("%Y-%m-%d"), day_names[weekday], day_type

WORDS = [
    {"word":"breakfast","phonetic":"/brekfest/","pos":"n.","meaning":"早饭，早餐","example":"I eat breakfast at 7 every morning.","example_zh":"我每天早上7点吃早饭。","tip":"break+fast=打破禁食的第一餐"},
    {"word":"homework","phonetic":"/houmwerk/","pos":"n.","meaning":"家庭作业","example":"I need to finish my homework before dinner.","example_zh":"我需要在晚饭前完成家庭作业。","tip":"home+work=在家做的工作"},
    {"word":"favorite","phonetic":"/feiverit/","pos":"adj.","meaning":"最喜欢的","example":"Blue is my favorite color.","example_zh":"蓝色是我最喜欢的颜色。","tip":"发音像飞我锐特"},
    {"word":"weather","phonetic":"/weder/","pos":"n.","meaning":"天气","example":"What is the weather like today?","example_zh":"今天天气怎么样？","tip":"和whether同音"},
    {"word":"together","phonetic":"/tegeder/","pos":"adv.","meaning":"一起，共同","example":"Lets play together after school.","example_zh":"放学后我们一起玩吧。","tip":"to+gether=聚集在一起"}
]

PHRASES = [
    {"phrase":"What time is it?","phonetic":"/wot taim iz it/","meaning":"现在几点了？","scene":"想知道时间时","example":"What time is it now?","example_zh":"现在几点了？","tip":"time是时间，what是什么"},
    {"phrase":"I am hungry.","phonetic":"/ai em hangri/","meaning":"我饿了。","scene":"肚子饿时","example":"Mom, I am hungry, can I eat something?","example_zh":"妈妈我饿了，能吃点东西吗？","tip":"hungry=饿，像航格瑞"},
    {"phrase":"Can you help me?","phonetic":"/ken ju help mi/","meaning":"你能帮我吗？","scene":"需要帮忙时","example":"Can you help me with this problem?","example_zh":"你能帮我解这道题吗？","tip":"help=帮助"},
    {"phrase":"I do not understand.","phonetic":"/ai dont understend/","meaning":"我不明白。","scene":"没听懂时","example":"Sorry, I do not understand, can you say it again?","example_zh":"抱歉我不明白，能再说一遍吗？","tip":"understand=理解"},
    {"phrase":"See you tomorrow!","phonetic":"/si ju temoro/","meaning":"明天见！","scene":"告别时","example":"Bye! See you tomorrow!","example_zh":"再见！明天见！","tip":"see=看见，tomorrow=明天"}
]
CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#e0f7fa 0%,#bbdefb 100%);min-height:100vh;padding:20px}
.container{max-width:800px;margin:0 auto}
.header{text-align:center;margin-bottom:30px;padding:20px;background:white;border-radius:20px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.header h1{color:#1565c0;font-size:2.2em;margin-bottom:10px}
.date-info{color:#666;font-size:1.1em}
.top-controls{display:flex;gap:10px;justify-content:center;margin-bottom:20px}
.word-card{background:white;border-radius:15px;padding:20px;margin-bottom:20px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.word-header{display:flex;align-items:center;gap:15px;margin-bottom:15px}
.word-number{width:40px;height:40px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:1.2em}
.word-title{flex:1}
.word-en{font-size:1.8em;color:#333;font-weight:bold}
.word-phonetic{color:#666;font-size:1em;margin-top:5px}
.word-pos{color:#999;font-size:.9em;margin-top:3px}
.word-meaning{background:#f5f5f5;padding:12px;border-radius:10px;font-size:1.3em;color:#333;margin-bottom:15px}
.word-scene{background:#e3f2fd;padding:10px;border-radius:8px;color:#1565c0;margin-bottom:10px}
.word-example{background:#fff3e0;padding:15px;border-radius:10px;margin-bottom:15px}
.example-en{color:#333;font-size:1.1em;margin-bottom:8px}
.example-zh{color:#666}
.word-tip{background:#e8f5e9;padding:10px;border-radius:8px;color:#2e7d32;margin-bottom:15px}
.controls{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.btn{padding:8px 16px;border:none;border-radius:20px;cursor:pointer;font-size:.9em;transition:all .3s}
.btn:hover{transform:translateY(-2px);box-shadow:0 4px 8px rgba(0,0,0,.2)}
.btn-slow{background:#ff9800;color:white}
.btn-normal{background:#2196f3;color:white}
.btn-fast{background:#4caf50;color:white}
.btn-stop{background:#f44336;color:white}
.btn-primary{background:#667eea;color:white;padding:12px 24px;font-size:1em}
.btn-secondary{background:#764ba2;color:white;padding:12px 24px;font-size:1em}"""

JS = """let isPlaying=false;
function speak(text,speed){
  window.speechSynthesis.cancel();
  let rate=speed==='slow'?0.7:speed==='fast'?1.0:0.85;
  for(let i=0;i<3;i++){
    const u=new SpeechSynthesisUtterance(text);
    u.lang='en-US';u.rate=rate;
    const vv=window.speechSynthesis.getVoices();
    const v=vv.find(v=>v.name.includes('Jenny'))||vv.find(v=>v.name.includes('Aria'))||vv.find(v=>v.name.includes('Google US English'))||vv[0];
    if(v)u.voice=v;
    window.speechSynthesis.speak(u);
  }
}
function stopSpeaking(){window.speechSynthesis.cancel();isPlaying=false;}
async function startAutoPlay(){
  if(isPlaying)return;isPlaying=true;
  const cards=document.querySelectorAll('.word-card');
  while(isPlaying){
    for(let c of cards){
      if(!isPlaying)break;
      await sp(c.querySelector('.word-en').textContent,'slow');
      await sl(800);
      await sp(c.querySelector('.example-en').textContent,'normal');
      await sl(2000);
    }
  }
}
function sp(t,s){return new Promise(r=>{const u=new SpeechSynthesisUtterance(t);u.lang='en-US';u.rate=s==='slow'?0.7:0.85;u.onend=r;window.speechSynthesis.speak(u);})}
function sl(ms){return new Promise(r=>setTimeout(r,ms))}
function goBack(){window.location.href='./index.html'}"""
def build_card(i, item, day_type):
    if day_type == "word":
        en = item["word"]
        ph = item["phonetic"]
        pos = item["pos"]
        scene_html = ""
    else:
        en = item["phrase"]
        ph = item["phonetic"]
        pos = "日常用语"
        scene_html = '<div class="word-scene">场景：' + item["scene"] + '</div>'
    
    sp_en = en.replace("'", " ")
    sp_ex = item["example"].replace("'", " ")
    
    return f'''<div class="word-card">
  <div class="word-header">
    <span class="word-number">0{i}</span>
    <div class="word-title">
      <div class="word-en">{en}</div>
      <div class="word-phonetic">{ph}</div>
      <div class="word-pos">{pos}</div>
    </div>
  </div>
  <div class="word-meaning">{item["meaning"]}</div>
  {scene_html}
  <div class="word-example">
    <div class="example-en">{item["example"]}</div>
    <div class="example-zh">{item["example_zh"]}</div>
  </div>
  <div class="word-tip">💡 {item["tip"]}</div>
  <div class="controls">
    <button class="btn btn-slow" onclick="speak('{sp_en}','slow')">🐢 慢速词×3</button>
    <button class="btn btn-normal" onclick="speak('{sp_en}','normal')">🚀 匀速词×3</button>
    <button class="btn btn-slow" onclick="speak('{sp_ex}','slow')">🐢 慢速句×3</button>
    <button class="btn btn-normal" onclick="speak('{sp_ex}','normal')">🚀 匀速句×3</button>
    <button class="btn btn-fast" onclick="speak('{sp_ex}','fast')">⚡ 常速句×3</button>
    <button class="btn btn-stop" onclick="stopSpeaking()">⏹ 停止</button>
  </div>
</div>'''

def gen_html(items, day_type, date_str, day_name):
    title = "📚 每日英语单词" if day_type == "word" else "💬 每日英语口语"
    cards = "".join([build_card(j+1, item, day_type) for j, item in enumerate(items)])
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} - {date_str}</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{title}</h1>
    <div class="date-info">{date_str} {day_name}</div>
  </div>
  <div class="top-controls">
    <button class="btn btn-primary" onclick="startAutoPlay()">▶️ 开始循环朗读</button>
    <button class="btn btn-secondary" onclick="goBack()">⬅️ 返回选择</button>
  </div>
  {cards}
</div>
<script>{JS}</script>
</body>
</html>'''
def gen_index(data):
    dj = json.dumps(data, ensure_ascii=False, indent=2)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>📚 每日英语学习</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}}
.container{{max-width:900px;margin:0 auto}}
.header{{text-align:center;margin-bottom:30px;color:white}}
.header h1{{font-size:2.5em;margin-bottom:10px;text-shadow:2px 2px 4px rgba(0,0,0,.3)}}
.header p{{font-size:1.2em;opacity:.9}}
.calendar{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px}}
.day-card{{background:white;border-radius:15px;padding:20px;box-shadow:0 4px 15px rgba(0,0,0,.2);cursor:pointer;transition:all .3s}}
.day-card:hover{{transform:translateY(-5px);box-shadow:0 8px 25px rgba(0,0,0,.3)}}
.day-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;padding-bottom:10px;border-bottom:2px solid #eee}}
.day-date{{font-size:1.1em;color:#667eea;font-weight:bold}}
.day-type{{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:4px 12px;border-radius:15px;font-size:.85em}}
.day-type.phrase{{background:linear-gradient(135deg,#f093fb,#f5576c)}}
.day-title{{font-size:1.2em;color:#333;margin-bottom:10px}}
.word-tag{{display:inline-block;background:#e3f2fd;color:#1565c0;padding:2px 8px;border-radius:10px;margin:2px;font-size:.85em}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📚 每日英语学习</h1>
    <p>小学五年级水平 · 每天进步一点点</p>
  </div>
  <div class="calendar" id="calendar"></div>
</div>
<script>
const DATA={dj};
function renderCalendar(){{
  const cal=document.getElementById('calendar');
  [...DATA].sort((a,b)=>new Date(b.date)-new Date(a.date)).forEach(day=>{{
    const card=document.createElement('div');
    card.className='day-card';
    card.onclick=()=>window.location.href=day.date+'.html';
    const tags=day.words.slice(0,3).map(w=>'<span class="word-tag">'+w.en+'</span>').join('');
    card.innerHTML='<div class="day-header"><span class="day-date">'+day.date+' '+day.day+'</span><span class="day-type '+day.type+'">'+(day.type==='word'?'单词':'口语')+'</span></div><div class="day-title">'+day.title+'</div><div>'+tags+'</div>';
    cal.appendChild(card);
  }});
}}
renderCalendar();
</script>
</body>
</html>'''

# Main program
date_str, day_name, day_type = get_day_info()
items = WORDS if day_type == "word" else PHRASES
print("Generating for", date_str, day_name, day_type)

# Generate daily page
html = gen_html(items, day_type, date_str, day_name)
with open(date_str + ".html", "w", encoding="utf-8") as f:
    f.write(html)
print("Generated:", date_str + ".html")

# Update index
data = []
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        src = f.read()
    m = re.search(r'const DATA=($$.*?$$);', src, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
        except:
            data = []

if day_type == "word":
    ww = [{"en": x["word"], "zh": x["meaning"]} for x in items]
    ss = [{"en": x["example"], "zh": x["example_zh"]} for x in items]
    title = "每日单词"
else:
    ww = [{"en": x["phrase"], "zh": x["meaning"]} for x in items]
    ss = [{"en": x["example"], "zh": x["example_zh"]} for x in items]
    title = "日常口语"

if not any(d["date"] == date_str for d in data):
    data.append({"date": date_str, "day": day_name, "type": day_type, "title": title, "words": ww, "sentences": ss})

with open("index.html", "w", encoding="utf-8") as f:
    f.write(gen_index(data))
print("Updated index.html")
