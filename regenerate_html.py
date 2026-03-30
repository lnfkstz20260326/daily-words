import json
import os
import re

# 读取修复后的素材库
print("读取修复后的素材库...")
with open('content_backup/content_backup.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

print(f"共有 {len(all_data)} 天的数据")

# HTML模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>每日英语口语 - {date}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    background: linear-gradient(135deg, #e0f7fa 0%, #bbdefb 100%);
    min-height: 100vh;
    padding: 10px;
}}
.container {{ max-width: 800px; margin: 0 auto; }}
.header {{
    text-align: center;
    margin-bottom: 15px;
    padding: 15px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,.1);
}}
.header h1 {{ color: #1565c0; font-size: 1.8em; margin-bottom: 8px; }}
.date-info {{ color: #666; font-size: 1em; }}

/* 顶部控制按钮 */
.top-controls {{
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 15px;
    flex-wrap: wrap;
}}
.loop-status {{
    background: #e8f5e9;
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    text-align: center;
    color: #2e7d32;
    font-weight: bold;
    display: none;
}}

/* 卡片 */
.card {{
    background: white;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,.1);
}}
.word-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}}
.word-number {{
    width: 35px;
    height: 35px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1em;
}}
.word-title {{
    flex: 1;
    font-size: 1.6em;
    color: #333;
    font-weight: bold;
}}
.phonetic {{
    color: #666;
    font-size: 0.9em;
}}
.word-meaning {{
    background: #f5f5f5;
    padding: 10px;
    border-radius: 8px;
    font-size: 1.2em;
    color: #333;
    margin-bottom: 12px;
}}
.part-of-speech {{
    background: #e3f2fd;
    color: #1976d2;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 14px;
}}
.chinese-meaning {{
    background: #ffebee;
    color: #c62828;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
}}
.memory-tip {{
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 16px;
    font-size: 15px;
    color: #2e7d32;
    border-left: 4px solid #4caf50;
}}
.example-box {{
    background: #f5f5f5;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 16px;
}}
.example-label {{
    color: #666;
    font-size: 0.9em;
    margin-bottom: 6px;
}}
.example-en {{
    color: #333;
    font-size: 1em;
    margin-bottom: 6px;
}}
.example-cn {{
    color: #666;
    font-size: 0.9em;
}}

/* 按钮 */
.button-group {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    justify-content: center;
}}
.btn {{
    padding: 6px 12px;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    font-size: 0.85em;
    transition: all 0.3s;
}}
.btn:hover {{ transform: scale(1.05); }}
.btn-slow {{ background: linear-gradient(135deg, #ff9800, #f57c00); color: white; }}
.btn-normal {{ background: linear-gradient(135deg, #2196f3, #1976d2); color: white; }}
.btn-fast {{ background: linear-gradient(135deg, #4caf50, #388e3c); color: white; }}
.btn-stop {{ background: linear-gradient(135deg, #f44336, #d32f2f); color: white; }}
.btn-loop {{ background: linear-gradient(135deg, #9c27b0, #7b1fa2); color: white; padding: 10px 20px; }}
.btn-secondary {{ background: linear-gradient(135deg, #764ba2, #6a3093); color: white; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📚 每日英语听说</h1>
        <div class="date-info">{date}</div>
    </div>

    <div class="top-controls">
        <button class="btn btn-loop" onclick="startAutoPlay()">
            ▶️ 开始循环朗读
        </button>
        <button class="btn btn-secondary" onclick="goBack()">
            ⬅️ 返回选择
        </button>
    </div>

    <div class="loop-status" id="loopStatus">🔄 播放中</div>

    {cards}

</div>

<script>
// ========== 全局变量 ==========
let isPlaying = false;
let currentLoop = 0;
const maxLoops = 7;
let allVoices = [];

// ========== 语音初始化 ==========
function initVoices() {{
    return new Promise((resolve) => {{
        allVoices = window.speechSynthesis.getVoices();
        if (allVoices.length > 0) {{
            resolve();
        }} else {{
            window.speechSynthesis.onvoiceschanged = () => {{
                allVoices = window.speechSynthesis.getVoices();
                resolve();
            }};
        }}
    }});
}}

// ========== 播放单个内容 ==========
function speak(text, lang, rate) {{
    return new Promise((resolve) => {{
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        utterance.rate = rate;
        
        // 选择语音
        if (lang === 'en-US') {{
            const voice = allVoices.find(v => v.lang.startsWith('en')) || allVoices[0];
            if (voice) utterance.voice = voice;
        }} else if (lang === 'zh-CN') {{
            const voice = allVoices.find(v => v.lang.startsWith('zh')) || allVoices[0];
            if (voice) utterance.voice = voice;
        }}
        
        utterance.onend = () => resolve();
        utterance.onerror = () => resolve();
        
        window.speechSynthesis.speak(utterance);
    }});
}}

// ========== 播放单词 ==========
async function playWord(wordEn, wordZh, speed) {{
    const isSlow = speed === 'slow';
    const rate = isSlow ? 0.4 : 0.8;
    
    // 播放3遍英语
    for (let i = 0; i < 3; i++) {{
        if (!isPlaying) return;
        await speak(wordEn, 'en-US', rate);
        await sleep(300);
    }}
    
    // 如果是慢速，播放汉语
    if (isSlow) {{
        await sleep(500);
        if (isPlaying) {{
            await speak(wordZh, 'zh-CN', 1.0);
        }}
    }}
}}

// ========== 播放句子 ==========
async function playSentence(exEn, exZh, speed) {{
    const isSlow = speed === 'slow';
    const isFast = speed === 'fast';
    let rate = isSlow ? 0.6 : (isFast ? 0.9 : 0.8);
    
    // 播放3遍英语
    for (let i = 0; i < 3; i++) {{
        if (!isPlaying) return;
        await speak(exEn, 'en-US', rate);
        await sleep(400);
    }}
    
    // 如果是慢速，播放汉语
    if (isSlow) {{
        await sleep(500);
        if (isPlaying) {{
            await speak(exZh, 'zh-CN', 1.0);
        }}
    }}
}}

// ========== 卡片按钮播放 ==========
async function playCard(cardIndex, type, speed) {{
    // 设置播放状态，允许中途停止
    isPlaying = true;
    
    const cards = document.querySelectorAll('.card');
    const card = cards[cardIndex];
    if (!card) return;
    
    const wordEn = card.querySelector('.word-title').textContent.trim();
    const wordZh = card.querySelector('.chinese-meaning').textContent.trim();
    const exEn = card.querySelector('.example-en').textContent.trim();
    const exZh = card.querySelector('.example-cn').textContent.trim();
    
    if (type === 'word') {{
        await playWord(wordEn, wordZh, speed);
    }} else {{
        await playSentence(exEn, exZh, speed);
    }}
}}

// ========== 停止播放 ==========
function stopSpeaking() {{
    isPlaying = false;
    window.speechSynthesis.cancel();
    const statusDiv = document.getElementById('loopStatus');
    if (statusDiv) {{
        statusDiv.style.display = 'block';
        statusDiv.textContent = '⏹ 已停止';
    }}
    const btn = document.querySelector('.btn-loop');
    if (btn) btn.textContent = '▶️ 开始循环朗读';
}}

// ========== 自动循环播放 ==========
async function startAutoPlay() {{
    // 如果已经在播放，点击变为暂停
    if (isPlaying) {{
        stopSpeaking();
        return;
    }}
    
    // 等待语音初始化
    await initVoices();
    
    isPlaying = true;
    currentLoop = 0;
    
    const statusDiv = document.getElementById('loopStatus');
    const btn = document.querySelector('.btn-loop');
    
    statusDiv.style.display = 'block';
    btn.textContent = '⏸ 暂停';
    
    const cards = document.querySelectorAll('.card');
    
    while (isPlaying && currentLoop < maxLoops) {{
        currentLoop++;
        statusDiv.textContent = `🔄 第 {{currentLoop}}/{{maxLoops}} 轮`;
        
        for (let i = 0; i < cards.length; i++) {{
            if (!isPlaying) break;
            
            const card = cards[i];
            const wordEn = card.querySelector('.word-title').textContent.trim();
            const wordZh = card.querySelector('.chinese-meaning').textContent.trim();
            const exEn = card.querySelector('.example-en').textContent.trim();
            const exZh = card.querySelector('.example-cn').textContent.trim();
            
            // 1. 慢速词×3 + 汉语
            for (let j = 0; j < 3; j++) {{
                if (!isPlaying) break;
                await speak(wordEn, 'en-US', 0.4);
                await sleep(300);
            }}
            if (isPlaying) {{
                await sleep(500);
                await speak(wordZh, 'zh-CN', 1.0);
                await sleep(300);
            }}
            
            // 2. 匀速词×3
            for (let j = 0; j < 3; j++) {{
                if (!isPlaying) break;
                await speak(wordEn, 'en-US', 0.8);
                await sleep(300);
            }}
            await sleep(300);
            
            // 3. 慢速句×3 + 汉语
            for (let j = 0; j < 3; j++) {{
                if (!isPlaying) break;
                await speak(exEn, 'en-US', 0.6);
                await sleep(400);
            }}
            if (isPlaying) {{
                await sleep(500);
                await speak(exZh, 'zh-CN', 1.0);
                await sleep(300);
            }}
            
            // 4. 匀速句×3
            for (let j = 0; j < 3; j++) {{
                if (!isPlaying) break;
                await speak(exEn, 'en-US', 0.8);
                await sleep(400);
            }}
            await sleep(300);
            
            // 5. 常速句×3
            for (let j = 0; j < 3; j++) {{
                if (!isPlaying) break;
                await speak(exEn, 'en-US', 0.9);
                await sleep(400);
            }}
            await sleep(500);
        }}
        
        // 每轮结束后等待2秒
        if (isPlaying && currentLoop < maxLoops) {{
            await sleep(2000);
        }}
    }}
    
    // 播放结束
    isPlaying = false;
    statusDiv.textContent = '✅ 完成';
    btn.textContent = '▶️ 开始循环朗读';
}}

// ========== 返回首页 ==========
function goBack() {{
    stopSpeaking();
    setTimeout(() => {{
        location.href = 'index.html';
    }}, 100);
}}

// ========== 工具函数 ==========
function sleep(ms) {{
    return new Promise(resolve => setTimeout(resolve, ms));
}}

// ========== 页面加载后初始化 ==========
initVoices();
</script>
</body>
</html>'''

def generate_card(word, index):
    """生成单个卡片HTML"""
    word_en = word.get('word_en', '')
    phonetic = word.get('phonetic', '')
    pos = word.get('pos', '')
    word_zh = word.get('word_zh', '')
    example_en = word.get('example_en', '')
    example_zh = word.get('example_zh', '')
    memory_tip = word.get('memory_tip', '')

    # 确保例句不为空
    if not example_en:
        example_en = f"This is {word_en}."
        example_zh = f"这是{word_zh}。"

    return f'''    <div class="card">
        <div class="word-header">
            <div class="word-number">{index:02d}</div>
            <div class="word-title">{word_en}</div>
            <span class="phonetic">{phonetic}</span>
        </div>
        <div class="word-meaning">
            <span class="part-of-speech">{pos}</span>
            <span class="chinese-meaning">{word_zh}</span>
        </div>
        <div class="memory-tip">{memory_tip if memory_tip else '💡 '}</div>
        <div class="example-box">
            <div class="example-label">例句 Example</div>
            <div class="example-en">{example_en}</div>
            <div class="example-cn">{example_zh}</div>
        </div>
        <div class="button-group">
            <button class="btn btn-slow" onclick="playCard({index-1}, 'word', 'slow')">🐢 慢速词×3</button>
            <button class="btn btn-normal" onclick="playCard({index-1}, 'word', 'normal')">🚀 匀速词×3</button>
            <button class="btn btn-slow" onclick="playCard({index-1}, 'sentence', 'slow')">🐢 慢速句×3</button>
            <button class="btn btn-normal" onclick="playCard({index-1}, 'sentence', 'normal')">🚀 匀速句×3</button>
            <button class="btn btn-fast" onclick="playCard({index-1}, 'sentence', 'fast')">⚡ 常速句×3</button>
            <button class="btn btn-stop" onclick="stopSpeaking()">⏹ 停止</button>
        </div>
    </div>'''

def generate_html(date, words):
    """生成单日HTML文件"""
    cards_html = '\n'.join([generate_card(w, i+1) for i, w in enumerate(words)])
    return HTML_TEMPLATE.format(date=date, cards=cards_html)

# 生成所有HTML文件
print("\n开始重新生成所有HTML文件...")
count = 0
for date, words in sorted(all_data.items()):
    filename = f"{date}.html"
    html = generate_html(date, words)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    count += 1
    if count <= 5 or count % 100 == 0:
        print(f"  已生成: {filename} ({len(words)} 个词)")

print(f"\n完成！共重新生成 {count} 个HTML文件")

# 验证2026-04-29
print("\n验证 2026-04-29.html:")
with open('2026-04-29.html', 'r', encoding='utf-8') as f:
    content = f.read()
    # 提取卡片数量
    cards = re.findall(r'<div class="card">', content)
    print(f"  卡片数量: {len(cards)}")
    
    # 提取单词
    words_in_html = re.findall(r'<div class="word-title">(.*?)</div>', content)
    print(f"  单词列表: {words_in_html}")
