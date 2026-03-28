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
<title>📚 每日英语学习 - 日期选择</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}}
.container{{max-width:1000px;margin:0 auto}}
.header{{text-align:center;margin-bottom:20px;color:white}}
.header h1{{font-size:2.2em;margin-bottom:10px;text-shadow:2px 2px 4px rgba(0,0,0,.3)}}
.header p{{font-size:1em;opacity:.9}}

/* 年份选择 */
.year-selector{{display:flex;justify-content:center;gap:15px;margin-bottom:20px;flex-wrap:wrap}}
.year-btn{{padding:10px 25px;border:none;border-radius:25px;background:rgba(255,255,255,.3);color:white;font-size:1.1em;cursor:pointer;transition:all .3s}}
.year-btn:hover,.year-btn.active{{background:white;color:#667eea;transform:scale(1.05)}}

/* 月份选择 */
.month-selector{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:20px;max-width:600px;margin-left:auto;margin-right:auto}}
.month-btn{{padding:8px;border:none;border-radius:8px;background:rgba(255,255,255,.2);color:white;font-size:.9em;cursor:pointer;transition:all .3s}}
.month-btn:hover,.month-btn.active{{background:#ff9800;transform:scale(1.05)}}

/* 日历网格 */
.calendar-container{{background:white;border-radius:20px;padding:20px;box-shadow:0 8px 30px rgba(0,0,0,.3)}}
.calendar-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;padding-bottom:10px;border-bottom:2px solid #eee}}
.calendar-title{{font-size:1.3em;color:#333;font-weight:bold}}
.weekdays{{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin-bottom:10px;text-align:center;font-weight:bold;color:#666}}
.days-grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:5px}}
.day-cell{{aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:10px;cursor:pointer;transition:all .3s;font-size:.85em;min-height:50px}}
.day-cell:hover{{transform:scale(1.1);box-shadow:0 4px 12px rgba(0,0,0,.2)}}
.day-cell.empty{{background:transparent;cursor:default}}
.day-cell.empty:hover{{transform:none;box-shadow:none}}
.day-cell.has-data{{background:linear-gradient(135deg,#667eea,#764ba2);color:white}}
.day-cell.no-data{{background:#f5f5f5;color:#999}}
.day-cell.selected{{background:#ff9800!important;color:white;box-shadow:0 0 0 3px #ff5722}}
.day-cell .day-num{{font-weight:bold;font-size:1.1em}}
.day-cell .day-type{{font-size:.7em;margin-top:2px}}

/* 底部按钮 */
.bottom-controls{{display:flex;justify-content:center;gap:20px;margin-top:20px}}
.control-btn{{padding:12px 40px;border:none;border-radius:30px;font-size:1.1em;cursor:pointer;transition:all .3s}}
.btn-confirm{{background:#4caf50;color:white}}
.btn-confirm:hover{{background:#45a049;transform:scale(1.05)}}
.btn-confirm:disabled{{background:#ccc;cursor:not-allowed;transform:none}}
.btn-today{{background:#2196f3;color:white}}
.btn-today:hover{{background:#1976d2;transform:scale(1.05)}}

/* 选中日期显示 */
.selected-info{{text-align:center;color:white;margin-top:15px;font-size:1.1em;min-height:30px}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📚 每日英语学习</h1>
    <p>小学五年级水平 · 选择日期开始学习</p>
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
const DATA = {dj};
const dataMap = {{}};
DATA.forEach(d => dataMap[d.date] = d);

let currentYear = 2026;
let currentMonth = 2; // 0-11
let selectedDate = null;

const years = [2026, 2027, 2028]; // 三年时间
const monthNames = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
const startDate = '2026-03-26'; // 数据开始日期

function init() {{
  renderYearSelector();
  renderMonthSelector();
  renderCalendar();
}}

function renderYearSelector() {{
  const container = document.getElementById('yearSelector');
  container.style.display = 'flex';
  container.innerHTML = years.map(y => 
    '<button class="year-btn ' + (y === currentYear ? 'active' : '') + '" onclick="selectYear(' + y + ')">' + y + '年</button>'
  ).join('');
}}

function renderMonthSelector() {{
  const container = document.getElementById('monthSelector');
  container.innerHTML = monthNames.map((m, i) => 
    '<button class="month-btn ' + (i === currentMonth ? 'active' : '') + '" onclick="selectMonth(' + i + ')">' + m + '</button>'
  ).join('');
}}

function renderCalendar() {{
  document.getElementById('calendarTitle').textContent = currentYear + '年' + monthNames[currentMonth];
  
  const firstDay = new Date(currentYear, currentMonth, 1).getDay();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  
  let html = '';
  // 空白格子
  for (let i = 0; i < firstDay; i++) {{
    html += '<div class="day-cell empty"></div>';
  }}
  
  // 日期格子
  for (let day = 1; day <= daysInMonth; day++) {{
    const dateStr = currentYear + '-' + String(currentMonth + 1).padStart(2, '0') + '-' + String(day).padStart(2, '0');
    const hasData = dataMap[dateStr];
    const isSelected = selectedDate === dateStr;
    const cellClass = 'day-cell ' + (hasData ? 'has-data' : 'no-data') + (isSelected ? ' selected' : '');
    const typeText = hasData ? (hasData.type === 'word' ? '单词' : '口语') : '';
    
    html += '<div class="' + cellClass + '" onclick="selectDate(\'' + dateStr + '\', ' + !!hasData + ')">' +
            '<span class="day-num">' + day + '</span>' +
            (typeText ? '<span class="day-type">' + typeText + '</span>' : '') +
            '</div>';
  }}
  
  document.getElementById('daysGrid').innerHTML = html;
}}

function selectYear(year) {{
  currentYear = year;
  renderYearSelector();
  renderCalendar();
}}

function selectMonth(month) {{
  currentMonth = month;
  renderMonthSelector();
  renderCalendar();
}}

function selectDate(dateStr, hasData) {{
  // 3月26日之前的日期不能选择
  if (dateStr < startDate) {{
    document.getElementById('selectedInfo').textContent = '⚠️ ' + dateStr + ' 暂无学习内容（3月26日开始）';
    document.getElementById('confirmBtn').disabled = true;
    selectedDate = null;
    renderCalendar();
    return;
  }}
  
  if (!hasData) {{
    selectedDate = dateStr;
    document.getElementById('selectedInfo').textContent = '⚠️ ' + dateStr + ' 暂无学习内容';
    document.getElementById('confirmBtn').disabled = true;
  }} else {{
    selectedDate = dateStr;
    const d = dataMap[dateStr];
    document.getElementById('selectedInfo').textContent = '✓ 已选择：' + dateStr + ' ' + d.day + ' · ' + (d.type === 'word' ? '单词' : '口语');
    document.getElementById('confirmBtn').disabled = false;
  }}
  renderCalendar();
}}

function confirmSelection() {{
  if (selectedDate) {{
    window.location.href = selectedDate + '.html';
  }}
}}

function goToToday() {{
  const today = new Date();
  currentYear = today.getFullYear();
  currentMonth = today.getMonth();
  renderYearSelector();
  renderMonthSelector();
  renderCalendar();
  
  const dateStr = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
  if (dataMap[dateStr]) {{
    selectDate(dateStr, true);
  }} else if (dateStr >= startDate) {{
    selectDate(dateStr, false);
  }}
}}

init();
</script>
</body>
</html>'''

# 历史数据（3月26日和3月27日）
HISTORY_DATA = [
    {
        "date": "2026-03-26",
        "day": "周四",
        "type": "word",
        "title": "每日单词",
        "words": [
            {"en": "encourage", "zh": "鼓励；给劲"},
            {"en": "patient", "zh": "有耐心的；不着急"},
            {"en": "remind", "zh": "提醒；告诉"},
            {"en": "curious", "zh": "好奇的；想知道"},
            {"en": "tidy", "zh": "整理；收拾"}
        ],
        "sentences": [
            {"en": "You're doing great! I'll always encourage you.", "zh": "你做得很好！我会一直鼓励你。"},
            {"en": "Be patient. Learning takes time.", "zh": "要有耐心。学习需要时间。"},
            {"en": "Let me remind you. Pack your bag.", "zh": "让我提醒你。收拾好你的书包。"},
            {"en": "You're so curious. Keep asking!", "zh": "你真好奇。继续问吧！"},
            {"en": "Can you tidy up your room?", "zh": "你能收拾一下你的房间吗？"}
        ]
    },
    {
        "date": "2026-03-27",
        "day": "周五",
        "type": "word",
        "title": "每日单词",
        "words": [
            {"en": "get up", "zh": "起床"},
            {"en": "wash face", "zh": "洗脸"},
            {"en": "brush teeth", "zh": "刷牙"},
            {"en": "eat breakfast", "zh": "吃早饭"},
            {"en": "go to school", "zh": "去上学"}
        ],
        "sentences": [
            {"en": "I get up at 7 o'clock every morning.", "zh": "我每天早上7点起床。"},
            {"en": "I wash my face with cold water.", "zh": "我用冷水洗脸。"},
            {"en": "I brush my teeth twice a day.", "zh": "我每天刷两次牙。"},
            {"en": "I eat breakfast at home.", "zh": "我在家吃早饭。"},
            {"en": "I go to school by bus.", "zh": "我乘公交车去上学。"}
        ]
    }
]

# Main program
date_str, day_name, day_type = get_day_info()
items = WORDS if day_type == "word" else PHRASES
print("Generating for", date_str, day_name, day_type)

# Generate daily page
html = gen_html(items, day_type, date_str, day_name)
with open(date_str + ".html", "w", encoding="utf-8") as f:
    f.write(html)
print("Generated:", date_str + ".html")

# 构建数据：历史数据 + 今天数据
data = list(HISTORY_DATA)  # 复制历史数据

if day_type == "word":
    ww = [{"en": x["word"], "zh": x["meaning"]} for x in items]
    ss = [{"en": x["example"], "zh": x["example_zh"]} for x in items]
    title = "每日单词"
else:
    ww = [{"en": x["phrase"], "zh": x["meaning"]} for x in items]
    ss = [{"en": x["example"], "zh": x["example_zh"]} for x in items]
    title = "日常口语"

# 检查今天是否已存在，不存在则添加
if not any(d["date"] == date_str for d in data):
    data.append({"date": date_str, "day": day_name, "type": day_type, "title": title, "words": ww, "sentences": ss})

with open("index.html", "w", encoding="utf-8") as f:
    f.write(gen_index(data))
print("Updated index.html with", len(data), "days of data")
