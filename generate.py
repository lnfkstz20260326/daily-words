"""
每日英语听说 - 页面生成器
基于3月28日稳定版本
循环次数：7次
"""

import datetime
import json
import os
import glob

# ==================== 配置 ====================
MAX_LOOPS = 7  # 循环次数
AUTO_DELAY_MS = 3000  # 页面加载后自动开始的时间（毫秒）
SPEED = 0.85  # 默认语速

# ==================== 数据定义 ====================
# 单词数据（周一到周五）
WORDS_DATA = {
    "周四": [
        {"en": "encourage", "zh": "鼓励；给劲", "phonetic": "/inkəˈrɪdʒ/", "pos": "v.", "example": "You're doing great! I'll always encourage you.", "example_zh": "你做得很好！我会一直鼓励你。", "tip": "en+courage=给勇气"},
        {"en": "patient", "zh": "有耐心的", "phonetic": "/ˈpeɪʃnt/", "pos": "adj.", "example": "Be patient. Learning takes time.", "example_zh": "要有耐心。学习需要时间。", "tip": "发音像陪申特"},
        {"en": "remind", "zh": "提醒", "phonetic": "/rɪˈmaɪnd/", "pos": "v.", "example": "Let me remind you. Pack your bag.", "example_zh": "让我提醒你。收拾好你的书包。", "tip": "re+mind=再次进入脑海"},
        {"en": "curious", "zh": "好奇的", "phonetic": "/ˈkjʊəriəs/", "pos": "adj.", "example": "You're so curious. Keep asking!", "example_zh": "你真好奇。继续问吧！", "tip": "发音像Q瑞尔斯"},
        {"en": "tidy", "zh": "整理；收拾", "phonetic": "/ˈtaɪdi/", "pos": "v.", "example": "Can you tidy up your room?", "example_zh": "你能收拾一下你的房间吗？", "tip": "发音像泰迪"}
    ],
    "周五": [
        {"en": "get up", "zh": "起床", "phonetic": "/ɡet ʌp/", "pos": "v.", "example": "I get up at 7 o'clock every morning.", "example_zh": "我每天早上7点起床。", "tip": "get得到，up向上"},
        {"en": "wash face", "zh": "洗脸", "phonetic": "/wɒʃ feɪs/", "pos": "v.", "example": "I wash my face with cold water.", "example_zh": "我用冷水洗脸。", "tip": "wash洗，face脸"},
        {"en": "brush teeth", "zh": "刷牙", "phonetic": "/brʌʃ ti:θ/", "pos": "v.", "example": "I brush my teeth twice a day.", "example_zh": "我每天刷两次牙。", "tip": "brush刷子，teeth牙齿"},
        {"en": "eat breakfast", "zh": "吃早饭", "phonetic": "/i:t ˈbrekfəst/", "pos": "v.", "example": "I eat breakfast at home.", "example_zh": "我在家吃早饭。", "tip": "eat吃，breakfast早餐"},
        {"en": "go to school", "zh": "去上学", "phonetic": "/ɡəʊ tu: sku:l/", "pos": "v.", "example": "I go to school by bus.", "example_zh": "我乘公交车去上学。", "tip": "go去，school学校"}
    ]
}

# 短语数据（周六、周日）
PHRASES_DATA = {
    "周六": [
        {"en": "What time is it?", "zh": "现在几点了？", "phonetic": "/wɒt taɪm ɪz ɪt/", "scene": "想知道时间时", "example": "What time is it? It's seven o'clock.", "example_zh": "现在几点了？七点了。", "tip": "time是时间"},
        {"en": "I'm hungry.", "zh": "我饿了。", "phonetic": "/aɪm ˈhʌŋɡri/", "scene": "肚子饿时", "example": "I'm hungry. Let's have lunch.", "example_zh": "我饿了。我们吃午饭吧。", "tip": "hungry=饿"},
        {"en": "Can you help me?", "zh": "你能帮我吗？", "phonetic": "/kæn ju: help mi/", "scene": "需要帮忙时", "example": "Can you help me with my homework?", "example_zh": "你能帮我做作业吗？", "tip": "help=帮助"},
        {"en": "I don't understand.", "zh": "我不明白。", "phonetic": "/aɪ dəʊnt ˌʌndəˈstænd/", "scene": "没听懂时", "example": "I don't understand. Can you say it again?", "example_zh": "我不明白。能再说一遍吗？", "tip": "understand=理解"},
        {"en": "See you tomorrow!", "zh": "明天见！", "phonetic": "/si: ju: təˈmɒrəʊ/", "scene": "告别时", "example": "Goodbye! See you tomorrow!", "example_zh": "再见！明天见！", "tip": "tomorrow=明天"}
    ],
    "周日": [
        {"en": "Let's go!", "zh": "走吧！出发！", "phonetic": "/lets ɡəʊ/", "scene": "出发时", "example": "Let's go! The movie starts soon.", "example_zh": "走吧！电影快开始了。", "tip": "let's=让我们"},
        {"en": "Good job!", "zh": "干得好！", "phonetic": "/ɡʊd dʒɒb/", "scene": "表扬时", "example": "Good job! You did it!", "example_zh": "干得好！你做到了！", "tip": "job=工作"},
        {"en": "Wait for me!", "zh": "等等我！", "phonetic": "/weɪt fɔ: mi/", "scene": "让人等待时", "example": "Wait for me! I'm coming!", "example_zh": "等等我！我来了！", "tip": "wait=等"},
        {"en": "How about you?", "zh": "你觉得怎么样？", "phonetic": "/haʊ əˈbaʊt ju/", "scene": "询问意见时", "example": "I like this book. How about you?", "example_zh": "我喜欢这本书。你呢？", "tip": "how about=...怎么样"},
        {"en": "Have a nice day!", "zh": "祝你有美好的一天！", "phonetic": "/hæv ə naɪs deɪ/", "scene": "告别时", "example": "Have a nice day! See you tomorrow!", "example_zh": "祝你有美好的一天！明天见！", "tip": "have a nice day=祝你好运"}
    ]
}

# ==================== 历史数据（3月26日-3月29日）====================
HISTORY_DATES = [
    {
        "date": "2026-03-26",
        "day": "周四",
        "type": "word",
        "title": "每日单词",
        "words": [
            {"en": "encourage", "zh": "鼓励；给劲", "phonetic": "/inkəˈrɪdʒ/", "pos": "v.", "example": "You're doing great! I'll always encourage you.", "example_zh": "你做得很好！我会一直鼓励你。", "tip": "en+courage=给勇气"},
            {"en": "patient", "zh": "有耐心的", "phonetic": "/ˈpeɪʃnt/", "pos": "adj.", "example": "Be patient. Learning takes time.", "example_zh": "要有耐心。学习需要时间。", "tip": "发音像陪申特"},
            {"en": "remind", "zh": "提醒", "phonetic": "/rɪˈmaɪnd/", "pos": "v.", "example": "Let me remind you. Pack your bag.", "example_zh": "让我提醒你。收拾好你的书包。", "tip": "re+mind=再次进入脑海"},
            {"en": "curious", "zh": "好奇的", "phonetic": "/ˈkjʊəriəs/", "pos": "adj.", "example": "You're so curious. Keep asking!", "example_zh": "你真好奇。继续问吧！", "tip": "发音像Q瑞尔斯"},
            {"en": "tidy", "zh": "整理；收拾", "phonetic": "/ˈtaɪdi/", "pos": "v.", "example": "Can you tidy up your room?", "example_zh": "你能收拾一下你的房间吗？", "tip": "发音像泰迪"}
        ]
    },
    {
        "date": "2026-03-27",
        "day": "周五",
        "type": "word",
        "title": "每日单词",
        "words": [
            {"en": "get up", "zh": "起床", "phonetic": "/ɡet ʌp/", "pos": "v.", "example": "I get up at 7 o'clock every morning.", "example_zh": "我每天早上7点起床。", "tip": "get得到，up向上"},
            {"en": "wash face", "zh": "洗脸", "phonetic": "/wɒʃ feɪs/", "pos": "v.", "example": "I wash my face with cold water.", "example_zh": "我用冷水洗脸。", "tip": "wash洗，face脸"},
            {"en": "brush teeth", "zh": "刷牙", "phonetic": "/brʌʃ ti:θ/", "pos": "v.", "example": "I brush my teeth twice a day.", "example_zh": "我每天刷两次牙。", "tip": "brush刷子，teeth牙齿"},
            {"en": "eat breakfast", "zh": "吃早饭", "phonetic": "/i:t ˈbrekfəst/", "pos": "v.", "example": "I eat breakfast at home.", "example_zh": "我在家吃早饭。", "tip": "eat吃，breakfast早餐"},
            {"en": "go to school", "zh": "去上学", "phonetic": "/ɡəʊ tu: sku:l/", "pos": "v.", "example": "I go to school by bus.", "example_zh": "我乘公交车去上学。", "tip": "go去，school学校"}
        ]
    },
    {
        "date": "2026-03-28",
        "day": "周六",
        "type": "phrase",
        "title": "每日英语口语",
        "words": [
            {"en": "What time is it?", "zh": "现在几点了？", "phonetic": "/wɒt taɪm ɪz ɪt/", "scene": "想知道时间时", "example": "What time is it? It's seven o'clock.", "example_zh": "现在几点了？七点了。", "tip": "time是时间"},
            {"en": "I'm hungry.", "zh": "我饿了。", "phonetic": "/aɪm ˈhʌŋɡri/", "scene": "肚子饿时", "example": "I'm hungry. Let's have lunch.", "example_zh": "我饿了。我们吃午饭吧。", "tip": "hungry=饿"},
            {"en": "Can you help me?", "zh": "你能帮我吗？", "phonetic": "/kæn ju: help mi/", "scene": "需要帮忙时", "example": "Can you help me with my homework?", "example_zh": "你能帮我做作业吗？", "tip": "help=帮助"},
            {"en": "I don't understand.", "zh": "我不明白。", "phonetic": "/aɪ dəʊnt ˌʌndəˈstænd/", "scene": "没听懂时", "example": "I don't understand. Can you say it again?", "example_zh": "我不明白。能再说一遍吗？", "tip": "understand=理解"},
            {"en": "See you tomorrow!", "zh": "明天见！", "phonetic": "/si: ju: təˈmɒrəʊ/", "scene": "告别时", "example": "Goodbye! See you tomorrow!", "example_zh": "再见！明天见！", "tip": "tomorrow=明天"}
        ]
    },
    {
        "date": "2026-03-29",
        "day": "周日",
        "type": "phrase",
        "title": "每日英语口语",
        "words": [
            {"en": "Let's go!", "zh": "走吧！出发！", "phonetic": "/lets ɡəʊ/", "scene": "出发时", "example": "Let's go! The movie starts soon.", "example_zh": "走吧！电影快开始了。", "tip": "let's=让我们"},
            {"en": "Good job!", "zh": "干得好！", "phonetic": "/ɡʊd dʒɒb/", "scene": "表扬时", "example": "Good job! You did it!", "example_zh": "干得好！你做到了！", "tip": "job=工作"},
            {"en": "Wait for me!", "zh": "等等我！", "phonetic": "/weɪt fɔ: mi/", "scene": "让人等待时", "example": "Wait for me! I'm coming!", "example_zh": "等等我！我来了！", "tip": "wait=等"},
            {"en": "How about you?", "zh": "你觉得怎么样？", "phonetic": "/haʊ əˈbaʊt ju/", "scene": "询问意见时", "example": "I like this book. How about you?", "example_zh": "我喜欢这本书。你呢？", "tip": "how about=...怎么样"},
            {"en": "Have a nice day!", "zh": "祝你有美好的一天！", "phonetic": "/hæv ə naɪs deɪ/", "scene": "告别时", "example": "Have a nice day! See you tomorrow!", "example_zh": "祝你有美好的一天！明天见！", "tip": "have a nice day=祝你好运"}
        ]
    }
]

# ==================== HTML 模板 ====================
CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#e0f7fa 0%,#bbdefb 100%);min-height:100vh;padding:20px}
.container{max-width:900px;margin:0 auto}
.header{text-align:center;margin-bottom:30px;padding:20px;background:white;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.header h1{font-size:2em;color:#1565c0;margin-bottom:10px}
.header .subtitle{color:#666;font-size:1em}
.notice{background:#e8f5e9;border:1px solid #a5d6a7;border-radius:8px;padding:10px 20px;text-align:center;color:#2e7d32;margin-bottom:20px;font-size:.9em}
.control-panel{display:flex;justify-content:center;gap:15px;margin-bottom:20px;flex-wrap:wrap}
.btn{padding:12px 24px;border:none;border-radius:25px;cursor:pointer;font-size:1em;font-weight:500;transition:all .3s;display:flex;align-items:center;gap:8px}
.btn:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.2)}
.btn-primary{background:linear-gradient(135deg,#667eea,#764ba2);color:white}
.btn-secondary{background:#764ba2;color:white}
.loop-status{background:#e8f5e9;border:1px solid #a5d6a7;border-radius:8px;padding:12px 20px;text-align:center;color:#2e7d32;font-weight:bold;margin-bottom:20px;display:none}
.word-card{background:white;border-radius:15px;padding:20px;margin-bottom:20px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.word-header{display:flex;align-items:center;gap:15px;margin-bottom:15px}
.word-number{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:1.1em}
.word-number.n1{background:#ff9800}.word-number.n2{background:#9c27b0}.word-number.n3{background:#f44336}.word-number.n4{background:#2196f3}.word-number.n5{background:#4caf50}
.word-title{font-size:1.8em;font-weight:700;color:#333}
.phonetic{color:#666;font-size:1em;margin-left:51px;margin-bottom:10px;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif}
.word-meaning{margin-left:51px;margin-bottom:15px}
.tag{display:inline-block;padding:3px 10px;border-radius:4px;font-size:.8em;margin-right:8px}
.tag-type{background:#e3f2fd;color:#1976d2}
.tag-meaning{background:#ffebee;color:#c62828;font-weight:600}
.sentence-section{margin-left:51px;background:#f5f5f5;padding:15px;border-radius:8px;margin-bottom:15px}
.sentence-label{color:#999;font-size:.85em;margin-bottom:8px}
.sentence-en{color:#333;font-size:1.1em;margin-bottom:5px}
.sentence-zh{color:#666;font-size:.95em}
.button-row{margin-left:51px;display:flex;gap:10px;flex-wrap:wrap}
.btn-small{padding:8px 16px;border:none;border-radius:20px;cursor:pointer;font-size:13px;font-weight:500;transition:all .2s;display:flex;align-items:center;gap:4px}
.btn-small:hover{transform:translateY(-1px);box-shadow:0 2px 8px rgba(0,0,0,.15)}
.btn-orange{background:#ff9800;color:white}.btn-orange:hover{background:#f57c00}
.btn-blue{background:#2196f3;color:white}.btn-blue:hover{background:#1976d2}
.btn-green{background:#4caf50;color:white}.btn-green:hover{background:#43a047}
.btn-red{background:#f44336;color:white}.btn-red:hover{background:#e53935}
.browser-tip{background:#fff3e0;border:1px solid #ffb74d;border-radius:8px;padding:10px 15px;text-align:center;color:#e65100;margin-bottom:15px;font-size:.9em}"""

# 基于3月28日稳定版本的JS
JS = """let isLooping = false;
let currentLoop = 0;
const maxLoops = """ + str(MAX_LOOPS) + """;

function speak(text, rate) {
    return new Promise((resolve) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = rate;
        utterance.pitch = 1;
        
        const voices = speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Jenny')) ||
                              voices.find(v => v.name.includes('Aria')) ||
                              voices.find(v => v.name.includes('Google US English')) ||
                              voices.find(v => v.name.includes('Samantha')) ||
                              voices.find(v => v.lang.startsWith('en'));
        if (preferredVoice) utterance.voice = preferredVoice;
        
        utterance.onend = resolve;
        speechSynthesis.speak(utterance);
    });
}

function speakChinese(text) {
    return new Promise((resolve) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'zh-CN';
        utterance.rate = 1.0;
        
        const voices = speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Xiaoxiao')) ||
                              voices.find(v => v.name.includes('Huihui')) ||
                              voices.find(v => v.lang.startsWith('zh'));
        if (preferredVoice) utterance.voice = preferredVoice;
        
        utterance.onend = resolve;
        speechSynthesis.speak(utterance);
    });
}

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function speakPhrase(index, type, rate) {
    // 只停止语音，不改变循环状态
    speechSynthesis.cancel();
    const phrase = phrases[index];
    const text = type === 'word' ? phrase.en : phrase.example;
    const zhText = type === 'word' ? phrase.zh : phrase.example_zh;
    
    // 播放英语3遍
    for (let i = 0; i < 3; i++) {
        await speak(text, rate);
        if (i < 2) await wait(300);
    }
    
    // 慢速时播放中文（rate <= 0.6 时）
    if (rate <= 0.6) {
        await wait(500);
        await speakChinese(zhText);
    }
}

async function startLoopReading() {
    if (isLooping) return;
    isLooping = true;
    currentLoop = 0;
    
    const statusDiv = document.getElementById('loopStatus');
    const btn = document.getElementById('startBtn');
    statusDiv.style.display = 'block';
    
    async function loop() {
        if (!isLooping) return;
        if (currentLoop >= maxLoops) {
            isLooping = false;
            statusDiv.textContent = '✓ 已完成 ' + maxLoops + ' 轮循环';
            btn.textContent = '▶️ 开始循环朗读';
            return;
        }
        
        currentLoop++;
        statusDiv.textContent = '循环播放中（第' + currentLoop + '/' + maxLoops + '轮）';
        btn.textContent = '⏸ 暂停循环';
        
        for (let i = 0; i < phrases.length; i++) {
            if (!isLooping) return;
            
            // 1. 慢速词：40%速度读3遍英语 + 1遍汉语
            await speakPhrase(i, 'word', 0.4);
            await wait(500);
            
            // 2. 匀速词：80%速度读3遍英语（无汉语）
            await speakPhrase(i, 'word', 0.8);
            await wait(500);
            
            // 3. 慢速句：60%速度读3遍英语 + 1遍汉语
            await speakPhrase(i, 'sentence', 0.6);
            await wait(500);
            
            // 4. 匀速句：80%速度读3遍英语（无汉语）
            await speakPhrase(i, 'sentence', 0.8);
            await wait(500);
            
            // 5. 常速句：90%速度读3遍英语（无汉语）
            await speakPhrase(i, 'sentence', 0.9);
            
            if (i < phrases.length - 1) await wait(1000);
        }
        
        if (isLooping) {
            await wait(2000);
            loop();
        }
    }
    
    loop();
}

function stopSpeaking() {
    isLooping = false;
    speechSynthesis.cancel();
    const statusDiv = document.getElementById('loopStatus');
    const btn = document.getElementById('startBtn');
    if (statusDiv) statusDiv.textContent = '⏹ 已停止';
    if (btn) btn.textContent = '▶️ 开始循环朗读';
}

function goBack() {
    window.location.href = './index.html';
}

// 确保语音列表加载
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
}

// 页面加载后自动开始
setTimeout(() => {
    startLoopReading();
}, """ + str(AUTO_DELAY_MS) + """);"""

def get_day_type(day_name):
    """根据星期几判断是单词还是短语"""
    if day_name in ["周六", "周日"]:
        return "phrase"
    return "word"

def build_card(i, item, day_type):
    """构建单词/短语卡片HTML"""
    number_class = f"n{(i-1) % 5 + 1}"
    
    if day_type == "word":
        return f'''<div class="word-card">
    <div class="word-header">
        <span class="word-number {number_class}">{i:02d}</span>
        <div class="word-title">{item["en"]}</div>
    </div>
    <div class="phonetic">{item["phonetic"]}</div>
    <div class="word-meaning">
        <span class="tag tag-type">{item["pos"]}</span>
        <span class="tag tag-meaning">{item["zh"]}</span>
    </div>
    <div class="sentence-section">
        <div class="sentence-label">例句 Example</div>
        <div class="sentence-en">{item["example"]}</div>
        <div class="sentence-zh">{item["example_zh"]}</div>
    </div>
    <div class="button-row">
        <button class="btn-small btn-orange" onclick="speakPhrase({i-1}, 'word', 0.5)">🐢 慢速词×3</button>
        <button class="btn-small btn-blue" onclick="speakPhrase({i-1}, 'word', 0.85)">🚀 匀速词×3</button>
        <button class="btn-small btn-orange" onclick="speakPhrase({i-1}, 'sentence', 0.5)">🐢 慢速句×3</button>
        <button class="btn-small btn-blue" onclick="speakPhrase({i-1}, 'sentence', 0.85)">🚀 匀速句×3</button>
        <button class="btn-small btn-green" onclick="speakPhrase({i-1}, 'sentence', 1.0)">⚡ 常速句×3</button>
        <button class="btn-small btn-red" onclick="stopSpeaking()">⏹ 停止</button>
    </div>
</div>'''
    else:
        return f'''<div class="word-card">
    <div class="word-header">
        <span class="word-number {number_class}">{i:02d}</span>
        <div class="word-title">{item["en"]}</div>
    </div>
    <div class="phonetic">{item["phonetic"]}</div>
    <div class="word-meaning">
        <span class="tag tag-type">日常用语</span>
        <span class="tag tag-meaning">{item["zh"]}</span>
    </div>
    <div class="sentence-section">
        <div class="sentence-label">场景：{item.get("scene", "")}</div>
        <div class="sentence-en">{item["example"]}</div>
        <div class="sentence-zh">{item["example_zh"]}</div>
    </div>
    <div class="button-row">
        <button class="btn-small btn-orange" onclick="speakPhrase({i-1}, 'word', 0.5)">🐢 慢速词×3</button>
        <button class="btn-small btn-blue" onclick="speakPhrase({i-1}, 'word', 0.85)">🚀 匀速词×3</button>
        <button class="btn-small btn-orange" onclick="speakPhrase({i-1}, 'sentence', 0.5)">🐢 慢速句×3</button>
        <button class="btn-small btn-blue" onclick="speakPhrase({i-1}, 'sentence', 0.85)">🚀 匀速句×3</button>
        <button class="btn-small btn-green" onclick="speakPhrase({i-1}, 'sentence', 1.0)">⚡ 常速句×3</button>
        <button class="btn-small btn-red" onclick="stopSpeaking()">⏹ 停止</button>
    </div>
</div>'''

def gen_daily_html(data_item):
    """生成每日播放页面HTML"""
    date_str = data_item["date"]
    day_name = data_item["day"]
    day_type = data_item["type"]
    title = data_item["title"]
    words = data_item["words"]
    
    # 构建短语数组供JS使用
    phrases_json = json.dumps(words, ensure_ascii=False)
    
    # 构建卡片HTML
    cards = "".join([build_card(j+1, word, day_type) for j, word in enumerate(words)])
    
    html = f'''<!DOCTYPE html>
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
    <h1>📚 每日英语听说</h1>
    <div class="subtitle">{date_str} {day_name} · 碎片化听说，随时开口交流</div>
  </div>
  <div class="notice">🎯 学习目标：每天5个{'实用单词' if day_type=='word' else '日常口语'}，建立英语思维</div>
  <div class="browser-tip">💡 建议使用 Edge 浏览器，语音效果更好！</div>
  <div class="loop-status" id="loopStatus"></div>
  <div class="control-panel">
    <button class="btn btn-primary" id="startBtn" onclick="startLoopReading()">▶️ 开始循环朗读</button>
    <button class="btn btn-secondary" onclick="goBack()">⬅️ 返回选择</button>
  </div>
  {cards}
</div>
<script>
const phrases = {phrases_json};
{JS}
</script>
</body>
</html>'''
    return html

def gen_index(data_list):
    """生成首页日历HTML"""
    dj = json.dumps(data_list, ensure_ascii=False, indent=2)
    html = '''<!DOCTYPE html>
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
.year-selector{display:flex;justify-content:center;gap:10px;margin-bottom:10px;flex-wrap:wrap}
.year-btn{padding:8px 20px;border:none;border-radius:20px;background:rgba(255,255,255,.3);color:white;font-size:1em;cursor:pointer;transition:all .3s}
.year-btn:hover,.year-btn.active{background:white;color:#667eea;transform:scale(1.05)}
.month-selector{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:10px;max-width:500px;margin-left:auto;margin-right:auto}
.month-btn{padding:6px;border:none;border-radius:6px;background:rgba(255,255,255,.2);color:white;font-size:.8em;cursor:pointer;transition:all .3s}
.month-btn:hover,.month-btn.active{background:#ff9800;transform:scale(1.05)}
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
.bottom-controls{display:flex;justify-content:center;gap:15px;margin-top:10px}
.control-btn{padding:10px 30px;border:none;border-radius:25px;font-size:1em;cursor:pointer;transition:all .3s}
.btn-confirm{background:#4caf50;color:white}
.btn-confirm:hover{background:#45a049;transform:scale(1.05)}
.btn-confirm:disabled{background:#ccc;cursor:not-allowed;transform:none}
.btn-today{background:#2196f3;color:white}
.btn-today:hover{background:#1976d2;transform:scale(1.05)}
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
let currentMonth = 2;
let selectedDate = null;

const years = [2026, 2027, 2028];
const monthNames = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
const startDate = '2026-03-26';

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
  for (let i = 0; i < firstDay; i++) {
    html += '<div class="day-cell empty"></div>';
  }
  
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
    return html

# ==================== 主程序 ====================
def main():
    print("=" * 60)
    print("每日英语听说 - 页面生成器")
    print("=" * 60)
    print(f"循环次数: {MAX_LOOPS} 次")
    print(f"自动开始延迟: {AUTO_DELAY_MS/1000} 秒")
    print()
    
    # 输出目录 - GitHub Actions 时为当前目录，本地运行时为指定目录
    if os.path.exists("/home/runner/work"):
        output_dir = "."  # GitHub Actions
    else:
        output_dir = r"C:\Users\Lenovo\WorkBuddy\automation-claw-20260327083500\.workbuddy\daily-words"
    
    # 生成所有历史日期的HTML
    for data in HISTORY_DATES:
        date_str = data["date"]
        filename = os.path.join(output_dir, f"{date_str}.html")
        
        print(f"生成: {filename}")
        html = gen_daily_html(data)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
    
    # 生成首页
    index_file = os.path.join(output_dir, "index.html")
    print(f"生成: {index_file}")
    
    # 构建首页数据
    index_data = []
    for data in HISTORY_DATES:
        index_data.append({
            "date": data["date"],
            "day": data["day"],
            "type": data["type"],
            "title": data["title"]
        })
    
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(gen_index(index_data))
    
    print()
    print("=" * 60)
    print("完成！")
    print(f"生成了 {len(HISTORY_DATES)} 个日期页面 + 1 个首页")
    print("=" * 60)

if __name__ == "__main__":
    main()
