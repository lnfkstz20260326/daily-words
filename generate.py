import datetime
import json
import os
import re
import glob

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

# 历史数据（3月26日和3月27日）- 用于生成历史HTML文件
HISTORY_DATA = [
    {
        "date": "2026-03-26",
        "day": "周四",
        "type": "word",
        "title": "每日单词",
        "words": [
            {"en": "encourage", "zh": "鼓励；给劲", "phonetic": "/inkaridz/", "pos": "v.", "example": "You're doing great! I'll always encourage you.", "example_zh": "你做得很好！我会一直鼓励你。", "tip": "en+courage=给勇气"},
            {"en": "patient", "zh": "有耐心的；不着急", "phonetic": "/peishent/", "pos": "adj.", "example": "Be patient. Learning takes time.", "example_zh": "要有耐心。学习需要时间。", "tip": "发音像陪申特"},
            {"en": "remind", "zh": "提醒；告诉", "phonetic": "/rimaind/", "pos": "v.", "example": "Let me remind you. Pack your bag.", "example_zh": "让我提醒你。收拾好你的书包。", "tip": "re+mind=再次进入脑海"},
            {"en": "curious", "zh": "好奇的；想知道", "phonetic": "/kjurias/", "pos": "adj.", "example": "You're so curious. Keep asking!", "example_zh": "你真好奇。继续问吧！", "tip": "发音像Q瑞尔斯"},
            {"en": "tidy", "zh": "整理；收拾", "phonetic": "/taidi/", "pos": "v.", "example": "Can you tidy up your room?", "example_zh": "你能收拾一下你的房间吗？", "tip": "发音像泰迪"}
        ]
    },
    {
        "date": "2026-03-27",
        "day": "周五",
        "type": "word",
        "title": "每日单词",
        "words": [
            {"en": "get up", "zh": "起床", "phonetic": "/get ap/", "pos": "v.", "example": "I get up at 7 o'clock every morning.", "example_zh": "我每天早上7点起床。", "tip": "get得到，up向上"},
            {"en": "wash face", "zh": "洗脸", "phonetic": "/wos feis/", "pos": "v.", "example": "I wash my face with cold water.", "example_zh": "我用冷水洗脸。", "tip": "wash洗，face脸"},
            {"en": "brush teeth", "zh": "刷牙", "phonetic": "/bras ti:th/", "pos": "v.", "example": "I brush my teeth twice a day.", "example_zh": "我每天刷两次牙。", "tip": "brush刷子，teeth牙齿"},
            {"en": "eat breakfast", "zh": "吃早饭", "phonetic": "/i:t brekfest/", "pos": "v.", "example": "I eat breakfast at home.", "example_zh": "我在家吃早饭。", "tip": "eat吃，breakfast早餐"},
            {"en": "go to school", "zh": "去上学", "phonetic": "/gou tu sku:l/", "pos": "v.", "example": "I go to school by bus.", "example_zh": "我乘公交车去上学。", "tip": "go去，school学校"}
        ]
    }
]

# 3月28日的数据（今天）
TODAY_DATA = {
    "date": "2026-03-28",
    "day": "周六",
    "type": "phrase",
    "title": "每日英语口语",
    "words": [
        {"en": "What time is it?", "zh": "现在几点了？", "phonetic": "/wot taim iz it/", "scene": "想知道时间时", "example": "What time is it now?", "example_zh": "现在几点了？", "tip": "time是时间，what是什么"},
        {"en": "I am hungry.", "zh": "我饿了。", "phonetic": "/ai em hangri/", "scene": "肚子饿时", "example": "Mom, I am hungry, can I eat something?", "example_zh": "妈妈我饿了，能吃点东西吗？", "tip": "hungry=饿，像航格瑞"},
        {"en": "Can you help me?", "zh": "你能帮我吗？", "phonetic": "/ken ju help mi/", "scene": "需要帮忙时", "example": "Can you help me with this problem?", "example_zh": "你能帮我解这道题吗？", "tip": "help=帮助"},
        {"en": "I do not understand.", "zh": "我不明白。", "phonetic": "/ai dont understend/", "scene": "没听懂时", "example": "Sorry, I do not understand, can you say it again?", "example_zh": "抱歉我不明白，能再说一遍吗？", "tip": "understand=理解"},
        {"en": "See you tomorrow!", "zh": "明天见！", "phonetic": "/si ju temoro/", "scene": "告别时", "example": "Bye! See you tomorrow!", "example_zh": "再见！明天见！", "tip": "see=看见，tomorrow=明天"}
    ]
}

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#e0f7fa 0%,#bbdefb 100%);min-height:100vh;padding:10px}
.container{max-width:800px;margin:0 auto}
.header{text-align:center;margin-bottom:15px;padding:15px;background:white;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.header h1{color:#1565c0;font-size:1.8em;margin-bottom:8px}
.date-info{color:#666;font-size:1em}
.top-controls{display:flex;gap:10px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}
.browser-tip{background:#fff3e0;padding:10px 15px;border-radius:8px;margin-bottom:15px;text-align:center;color:#e65100;font-size:.9em}
.loop-status{background:#e8f5e9;padding:10px 15px;border-radius:8px;margin-bottom:15px;text-align:center;color:#2e7d32;font-weight:bold;display:none}
.word-card{background:white;border-radius:15px;padding:15px;margin-bottom:15px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.word-header{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.word-number{width:35px;height:35px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:1em}
.word-title{flex:1}
.word-en{font-size:1.6em;color:#333;font-weight:bold}
.word-phonetic{color:#666;font-size:.9em;margin-top:3px}
.word-pos{color:#999;font-size:.85em;margin-top:2px}
.word-meaning{background:#f5f5f5;padding:10px;border-radius:8px;font-size:1.2em;color:#333;margin-bottom:12px}
.word-scene{background:#e3f2fd;padding:8px 12px;border-radius:6px;color:#1565c0;margin-bottom:10px;font-size:.9em}
.word-example{background:#fff3e0;padding:12px;border-radius:8px;margin-bottom:12px}
.example-en{color:#333;font-size:1em;margin-bottom:6px}
.example-zh{color:#666;font-size:.9em}
.word-tip{background:#e8f5e9;padding:8px 12px;border-radius:6px;color:#2e7d32;margin-bottom:12px;font-size:.9em}
.controls{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.btn{padding:6px 12px;border:none;border-radius:15px;cursor:pointer;font-size:.85em;transition:all .3s}
.btn:hover{transform:translateY(-2px);box-shadow:0 4px 8px rgba(0,0,0,.2)}
.btn-slow{background:#ff9800;color:white}
.btn-normal{background:#2196f3;color:white}
.btn-fast{background:#4caf50;color:white}
.btn-stop{background:#f44336;color:white}
.btn-primary{background:#667eea;color:white;padding:10px 20px;font-size:.95em}
.btn-secondary{background:#764ba2;color:white;padding:10px 20px;font-size:.95em}"""

JS = """let isPlaying=false,currentLoop=0,maxLoops=10;
function speakWord(wordEn,wordZh,speed){
  window.speechSynthesis.cancel();
  let rate=speed==='slow'?0.4:0.8;
  // 播放英语3遍
  for(let i=0;i<3;i++){
    const u=new SpeechSynthesisUtterance(wordEn);
    u.lang='en-US';u.rate=rate;
    const vv=window.speechSynthesis.getVoices();
    const v=vv.find(v=>v.name.includes('Jenny'))||vv.find(v=>v.name.includes('Aria'))||vv.find(v=>v.name.includes('Google US English'))||vv[0];
    if(v)u.voice=v;
    window.speechSynthesis.speak(u);
  }
  // 只有慢速才播放汉语（延迟1.5秒后）
  if(speed==='slow'){
    setTimeout(()=>{
      const u2=new SpeechSynthesisUtterance(wordZh);
      u2.lang='zh-CN';u2.rate=1.0;
      window.speechSynthesis.speak(u2);
    },1500);
  }
}
function speakSentence(exEn,exZh,speed){
  window.speechSynthesis.cancel();
  let rate=speed==='slow'?0.6:speed==='fast'?0.9:0.8;
  // 播放英语3遍
  for(let i=0;i<3;i++){
    const u=new SpeechSynthesisUtterance(exEn);
    u.lang='en-US';u.rate=rate;
    const vv=window.speechSynthesis.getVoices();
    const v=vv.find(v=>v.name.includes('Jenny'))||vv.find(v=>v.name.includes('Aria'))||vv.find(v=>v.name.includes('Google US English'))||vv[0];
    if(v)u.voice=v;
    window.speechSynthesis.speak(u);
  }
  // 只有慢速才播放汉语（延迟2秒后）
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
  const statusDiv=document.querySelector('.loop-status');
  statusDiv.style.display='block';
  statusDiv.textContent='⏹ 已停止';
  document.querySelector('.btn-primary').textContent='▶️ 开始循环朗读';
}
async function startAutoPlay(){
  if(isPlaying)return;
  isPlaying=true;
  currentLoop=0;
  const statusDiv=document.querySelector('.loop-status');
  const btn=document.querySelector('.btn-primary');
  statusDiv.style.display='block';
  const cards=document.querySelectorAll('.word-card');
  while(isPlaying&&currentLoop<maxLoops){
    currentLoop++;
    statusDiv.textContent='循环播放中（第'+currentLoop+'/'+maxLoops+'轮）';
    btn.textContent='⏸ 暂停循环';
    for(let c of cards){
      if(!isPlaying)break;
      const wordEn=c.querySelector('.word-en').textContent;
      const wordZh=c.querySelector('.word-meaning').textContent;
      const exEn=c.querySelector('.example-en').textContent;
      const exZh=c.querySelector('.example-zh').textContent;
      // 1. 慢速词×3 + 汉语
      for(let i=0;i<3;i++){if(!isPlaying)break;await sp(wordEn,'slow');await sl(500);}
      if(isPlaying){await spZh(wordZh);await sl(500);}
      // 2. 匀速词×3 + 汉语
      for(let i=0;i<3;i++){if(!isPlaying)break;await sp(wordEn,'normal');await sl(500);}
      if(isPlaying){await spZh(wordZh);await sl(500);}
      // 3. 慢速句×3 + 汉语
      for(let i=0;i<3;i++){if(!isPlaying)break;await sp(exEn,'slow');await sl(600);}
      if(isPlaying){await spZh(exZh);await sl(500);}
      // 4. 匀速句×3 + 汉语
      for(let i=0;i<3;i++){if(!isPlaying)break;await sp(exEn,'normal');await sl(600);}
      if(isPlaying){await spZh(exZh);await sl(500);}
      // 5. 常速句×3（不加汉语）
      for(let i=0;i<3;i++){if(!isPlaying)break;await sp(exEn,'fast');await sl(500);}
      await sl(1000);
    }
    if(currentLoop>=maxLoops){
      isPlaying=false;
      statusDiv.textContent='✓ 已完成'+maxLoops+'轮循环';
      btn.textContent='▶️ 开始循环朗读';
    }
  }
}
function spZh(text){return new Promise(r=>{const u=new SpeechSynthesisUtterance(text);u.lang='zh-CN';u.rate=1.0;u.onend=r;window.speechSynthesis.speak(u);})}
function sp(t,s){return new Promise(r=>{const u=new SpeechSynthesisUtterance(t);u.lang='en-US';u.rate=s==='slow'?0.4:s==='fast'?0.9:0.8;u.onend=r;window.speechSynthesis.speak(u);})}
function sl(ms){return new Promise(r=>setTimeout(r,ms))}
function goBack(){window.location.href='./index.html'}"""

def build_card(i, item, day_type):
    if day_type == "word":
        en = item["en"]
        ph = item.get("phonetic", "")
        pos = item.get("pos", "")
        scene_html = ""
    else:
        en = item["en"]
        ph = item.get("phonetic", "")
        pos = "日常用语"
        scene_html = '<div class="word-scene">场景：' + item.get("scene", "") + '</div>'
    
    sp_en = en.replace("'", " ")
    sp_ex = item.get("example", "").replace("'", " ")
    
    return f'''<div class="word-card">
  <div class="word-header">
    <span class="word-number">{i:02d}</span>
    <div class="word-title">
      <div class="word-en">{en}</div>
      <div class="word-phonetic">{ph}</div>
      <div class="word-pos">{pos}</div>
    </div>
  </div>
  <div class="word-meaning">{item["zh"]}</div>
  {scene_html}
  <div class="word-example">
    <div class="example-en">{item.get("example", "")}</div>
    <div class="example-zh">{item.get("example_zh", "")}</div>
  </div>
  <div class="word-tip">💡 {item.get("tip", "")}</div>
  <div class="controls">
    <button class="btn btn-slow" onclick="speakWord('{sp_en}','{item["zh"]}','slow')">🐢 慢速词×3</button>
    <button class="btn btn-normal" onclick="speakWord('{sp_en}','{item["zh"]}','normal')">🚀 匀速词×3</button>
    <button class="btn btn-slow" onclick="speakSentence('{sp_ex}','{item["example_zh"]}','slow')">🐢 慢速句×3</button>
    <button class="btn btn-normal" onclick="speakSentence('{sp_ex}','{item["example_zh"]}','normal')">🚀 匀速句×3</button>
    <button class="btn btn-fast" onclick="speakSentence('{sp_ex}','{item["example_zh"]}','fast')">⚡ 常速句×3</button>
    <button class="btn btn-stop" onclick="stopSpeaking()">⏹ 停止</button>
  </div>
</div>'''

def gen_daily_html(data_item):
    """生成每日播放页面HTML"""
    date_str = data_item["date"]
    day_name = data_item["day"]
    day_type = data_item["type"]
    title = data_item["title"]
    words = data_item["words"]
    
    cards = "".join([build_card(j+1, word, day_type) for j, word in enumerate(words)])
    
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
    <div class="date-info">{date_str} {day_name} · 碎片化听说，随时开口交流</div>
  </div>
  <div class="browser-tip">💡 建议使用 Chrome 或 Edge 浏览器，语音效果更好！</div>
  <div class="loop-status"></div>
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
    """生成首页日历HTML"""
    dj = json.dumps(data, ensure_ascii=False, indent=2)
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>📚 每日英语听说 - 日期选择</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:10px}
.container{max-width:900px;margin:0 auto}
.header{text-align:center;margin-bottom:10px;color:white}
.header h1{font-size:1.8em;margin-bottom:5px;text-shadow:2px 2px 4px rgba(0,0,0,.3)}
.header p{font-size:.9em;opacity:.9}

/* 年份选择 */
.year-selector{display:flex;justify-content:center;gap:10px;margin-bottom:10px;flex-wrap:wrap}
.year-btn{padding:8px 20px;border:none;border-radius:20px;background:rgba(255,255,255,.3);color:white;font-size:1em;cursor:pointer;transition:all .3s}
.year-btn:hover,.year-btn.active{background:white;color:#667eea;transform:scale(1.05)}

/* 月份选择 */
.month-selector{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:10px;max-width:500px;margin-left:auto;margin-right:auto}
.month-btn{padding:6px;border:none;border-radius:6px;background:rgba(255,255,255,.2);color:white;font-size:.8em;cursor:pointer;transition:all .3s}
.month-btn:hover,.month-btn.active{background:#ff9800;transform:scale(1.05)}

/* 日历网格 */
.calendar-container{background:white;border-radius:12px;padding:8px;box-shadow:0 8px 30px rgba(0,0,0,.3)}
.calendar-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;padding-bottom:4px;border-bottom:2px solid #eee}
.calendar-title{font-size:1em;color:#333;font-weight:bold}
.weekdays{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;margin-bottom:4px;text-align:center;font-weight:bold;color:#666;font-size:.75em}
.days-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px}
.day-cell{aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:5px;cursor:pointer;transition:all .3s;font-size:.7em;min-height:28px;padding:1px}
.day-cell:hover{transform:scale(1.1);box-shadow:0 4px 12px rgba(0,0,0,.2)}
.day-cell.empty{background:transparent;cursor:default}
.day-cell.empty:hover{transform:none;box-shadow:none}
.day-cell.has-data{background:linear-gradient(135deg,#667eea,#764ba2);color:white}
.day-cell.no-data{background:#f5f5f5;color:#999}
.day-cell.selected{background:#ff9800!important;color:white;box-shadow:0 0 0 2px #ff5722}
.day-cell .day-num{font-weight:bold;font-size:1em}
.day-cell .day-type{font-size:.65em;margin-top:1px}

/* 底部按钮 */
.bottom-controls{display:flex;justify-content:center;gap:15px;margin-top:10px}
.control-btn{padding:10px 30px;border:none;border-radius:25px;font-size:1em;cursor:pointer;transition:all .3s}
.btn-confirm{background:#4caf50;color:white}
.btn-confirm:hover{background:#45a049;transform:scale(1.05)}
.btn-confirm:disabled{background:#ccc;cursor:not-allowed;transform:none}
.btn-today{background:#2196f3;color:white}
.btn-today:hover{background:#1976d2;transform:scale(1.05)}

/* 选中日期显示 */
.selected-info{text-align:center;color:white;margin-top:8px;font-size:1em;min-height:25px}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📚 每日英语听说</h1>
    <p>母语化练习，每日随听，明日常新</p>
  </div>
  
  <div class="year-selector" id="yearSelector"></div>
  <div class="month-selector" id="monthSelector"></div>
  
  <div class="calendar-container">
    <div class="calendar-header">
      <span class="calendar-title" id="calendarTitle">2026年3月</span>
    </div>
    <div class="weekdays">
      <div>日</div><div>一</div><div>二</div><div>三</div><div>四</div><div>五</div><div>六</div>
    </div>
    <div class="days-grid" id="daysGrid"></div>
  </div>
  
  <div class="selected-info" id="selectedInfo"></div>
  
  <div class="bottom-controls">
    <button class="control-btn btn-today" onclick="goToToday()">📅 今天</button>
    <button class="control-btn btn-confirm" id="confirmBtn" onclick="confirmSelection()" disabled>✓ 确定</button>
  </div>
</div>

<script>
const DATA = ''' + dj + ''';
const dataMap = {};
DATA.forEach(d => dataMap[d.date] = d);

let currentYear = 2026;
let currentMonth = 2; // 0-11
let selectedDate = null;

const years = [2026, 2027, 2028]; // 三年时间
const monthNames = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
const startDate = '2026-03-26'; // 数据开始日期

function init() {
  renderYearSelector();
  renderMonthSelector();
  renderCalendar();
}

function renderYearSelector() {
  const container = document.getElementById('yearSelector');
  container.style.display = 'flex';
  container.innerHTML = years.map(y => 
    '<button class="year-btn ' + (y === currentYear ? 'active' : '') + '" onclick="selectYear(' + y + ')">' + y + '年</button>'
  ).join('');
}

function renderMonthSelector() {
  const container = document.getElementById('monthSelector');
  container.innerHTML = monthNames.map((m, i) => 
    '<button class="month-btn ' + (i === currentMonth ? 'active' : '') + '" onclick="selectMonth(' + i + ')">' + m + '</button>'
  ).join('');
}

function renderCalendar() {
  document.getElementById('calendarTitle').textContent = currentYear + '年' + monthNames[currentMonth];
  
  const firstDay = new Date(currentYear, currentMonth, 1).getDay();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  
  let html = '';
  // 空白格子
  for (let i = 0; i < firstDay; i++) {
    html += '<div class="day-cell empty"></div>';
  }
  
  // 日期格子
  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = currentYear + '-' + String(currentMonth + 1).padStart(2, '0') + '-' + String(day).padStart(2, '0');
    const hasData = dataMap[dateStr];
    const isSelected = selectedDate === dateStr;
    const cellClass = 'day-cell ' + (hasData ? 'has-data' : 'no-data') + (isSelected ? ' selected' : '');
    
    html += '<div class="' + cellClass + '" onclick="selectDate(' + "'" + dateStr + "'" + ', ' + !!hasData + ')">' +
            '<span class="day-num">' + day + '</span>' +
            (hasData ? '<span class="day-type">听说</span>' : '') +
            '</div>';
  }
  
  document.getElementById('daysGrid').innerHTML = html;
}

function selectYear(year) {
  currentYear = year;
  renderYearSelector();
  renderCalendar();
}

function selectMonth(month) {
  currentMonth = month;
  renderMonthSelector();
  renderCalendar();
}

function selectDate(dateStr, hasData) {
  // 3月26日之前的日期不能选择
  if (dateStr < startDate) {
    document.getElementById('selectedInfo').textContent = '⚠️ ' + dateStr + ' 暂无学习内容（3月26日开始）';
    document.getElementById('confirmBtn').disabled = true;
    selectedDate = null;
    renderCalendar();
    return;
  }
  
  if (!hasData) {
    selectedDate = dateStr;
    document.getElementById('selectedInfo').textContent = '⚠️ ' + dateStr + ' 暂无学习内容';
    document.getElementById('confirmBtn').disabled = true;
  } else {
    selectedDate = dateStr;
    const d = dataMap[dateStr];
    document.getElementById('selectedInfo').textContent = '✓ 已选择：' + dateStr + ' ' + d.day + ' · 听说';
    document.getElementById('confirmBtn').disabled = false;
  }
  renderCalendar();
}

function confirmSelection() {
  if (selectedDate) {
    window.location.href = selectedDate + '.html';
  }
}

function goToToday() {
  const today = new Date();
  currentYear = today.getFullYear();
  currentMonth = today.getMonth();
  renderYearSelector();
  renderMonthSelector();
  renderCalendar();
  
  const dateStr = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
  if (dataMap[dateStr]) {
    selectDate(dateStr, true);
  } else if (dateStr >= startDate) {
    selectDate(dateStr, false);
  }
}

init();
</script>
</body>
</html>'''
    return html_template

def get_existing_dates():
    """获取已存在的HTML文件日期列表"""
    existing = []
    for f in glob.glob("*.html"):
        if f != "index.html" and re.match(r"\d{4}-\d{2}-\d{2}\.html", f):
            date_str = f.replace(".html", "")
            existing.append(date_str)
    return sorted(existing)

def build_data_from_history():
    """从历史数据构建数据列表"""
    data = []
    
    # 添加历史数据
    for h in HISTORY_DATA:
        data.append({
            "date": h["date"],
            "day": h["day"],
            "type": h["type"],
            "title": h["title"]
        })
    
    # 添加今天的数据
    data.append({
        "date": TODAY_DATA["date"],
        "day": TODAY_DATA["day"],
        "type": TODAY_DATA["type"],
        "title": TODAY_DATA["title"]
    })
    
    return data

# Main program
print("=" * 50)
print("每日英语听说页面生成器")
print("=" * 50)

# 获取已存在的日期
existing_dates = get_existing_dates()
print(f"已存在的日期文件: {existing_dates}")

# 构建完整数据列表
all_data = build_data_from_history()

# 生成所有历史日期的HTML文件（如果不存在）
for hist in HISTORY_DATA:
    date_str = hist["date"]
    filename = date_str + ".html"
    
    if date_str not in existing_dates:
        print(f"生成历史文件: {filename}")
        html = gen_daily_html(hist)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
    else:
        print(f"文件已存在，跳过: {filename}")

# 生成今天的HTML文件
today_filename = TODAY_DATA["date"] + ".html"
if TODAY_DATA["date"] not in existing_dates:
    print(f"生成今天文件: {today_filename}")
    html = gen_daily_html(TODAY_DATA)
    with open(today_filename, "w", encoding="utf-8") as f:
        f.write(html)
else:
    print(f"今天文件已存在，跳过: {today_filename}")

# 生成/更新首页
print(f"更新首页: index.html")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(gen_index(all_data))

print("=" * 50)
print(f"完成！共 {len(all_data)} 天的数据")
print(f"生成的文件: {', '.join([d['date'] + '.html' for d in all_data])}, index.html")
print("=" * 50)
