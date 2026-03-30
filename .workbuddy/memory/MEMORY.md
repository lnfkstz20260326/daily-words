# 每日英语听说 - 长期记忆

## 项目概述
**每日英语听说** - 一个自动生成每日英语学习页面的Web应用，部署在GitHub Pages上。

## 🔴 重要教训（2026-03-30）

### HTML修复注意事项
1. **top-controls位置**：必须放在header结束后、第一个card之前
2. **幂等修复脚本**：修复脚本必须能多次运行而不产生重复内容
3. **模板法修复**：使用正确的文件作为模板，然后用脚本批量应用到其他文件

### JS控制逻辑要点（3月29日稳定版）
- **变量**：`isPlaying`, `currentLoop`, `maxLoops=7`
- **函数**：
  - `speakWord(wordEn, wordZh, speed)`：播放单词，slow播放后异步播放汉语
  - `speakSentence(exEn, exZh, speed)`：播放句子，slow播放后异步播放汉语
  - `startAutoPlay()`：开始/暂停循环（检查isPlaying状态）
  - `stopSpeaking()`：停止所有播放
  - `goBack()`：停止播放+100ms延迟后跳转

### 🔴 3月29日稳定架构
```javascript
// 变量
let isPlaying=false, currentLoop=0, maxLoops=7;

// 顶部按钮
onclick="startAutoPlay()"

// 开始/暂停函数
async function startAutoPlay(){
  if(isPlaying){
    // 暂停
    isPlaying=false;
    window.speechSynthesis.cancel();
    ...
    return;
  }
  // 开始播放
  isPlaying=true;
  while(isPlaying && currentLoop < maxLoops){
    // 播放逻辑
  }
}

// 汉语播放（异步）
if(speed==='slow'){
  setTimeout(()=>{
    const u2=new SpeechSynthesisUtterance(wordZh);
    u2.lang='zh-CN';u2.rate=1.0;
    window.speechSynthesis.speak(u2);
  },1500);
}
```

## 核心信息

### 访问地址
- GitHub Pages：https://lnfkstz20260326.github.io/daily-words/
- GitHub仓库：https://github.com/lnfkstz20260326/daily-words

### 页面标题
- **首页标题**：📚 每日英语听说
- **首页副标题**：母语化练习，每日随听，明日常新
- **播放界面副标题**：碎片化听说，随时开口交流

### 朗读规则（重要！）
**5个按钮的功能：**
1. 🐢 慢速词×3：40%速度读3遍英语 + 1遍汉语
2. 🚀 匀速词×3：80%速度读3遍英语（无汉语）
3. 🐢 慢速句×3：60%速度读3遍英语 + 1遍汉语
4. 🚀 匀速句×3：80%速度读3遍英语（无汉语）
5. ⚡ 常速句×3：90%速度读3遍英语（无汉语）

**自动循环播放（7轮）：**
- 每轮依次播放5个按钮的内容
- 每个卡片之间间隔1秒，每轮结束后等待2秒
- 共7轮，页面加载后3秒自动开始

### 循环播放按钮
- **按钮位置**：页面顶部（在header下方）
- **返回按钮**：同样在顶部，便于返回选择日期
- 点击可暂停/恢复循环播放

### JS字段名对应关系（重要！）
phrase.en = 单词/短语本身
phrase.example = 例句
phrase.zh = 单词/短语的中文翻译
phrase.example_zh = 例句的中文翻译

### 技术架构
- **生成器**：generate.py（Python模板）
- **自动部署**：GitHub Actions（每天早上8点运行）
- **托管**：GitHub Pages

## 🔴 重要教训

### 2026-03-29 问题汇总
1. **字段名错误**：`phrase.word` → `phrase.en`，`phrase.sentence` → `phrase.example`
2. **循环中断问题**：stopSpeaking 只停止语音，不改变循环状态
3. **循环逻辑**：必须依次播放5个按钮的内容
4. **慢速条件**：`rate <= 0.6` 使0.4和0.6都能播放汉语

### 2026-03-30 修复
1. **汉语音频播放**：必须调用 `window.speechSynthesis.speak(cnUtterance)`
2. **循环按钮位置**：必须放在页面顶部（在header下方）
3. **返回按钮**：添加返回首页按钮
4. **幂等修复脚本**：修复脚本必须能多次运行而不产生重复
5. **记忆提示优化**：用英文思维记忆法替换所有"记住xxx英文表达"和简单翻译
6. **🔴 speakPhrase桥接函数**：卡片按钮调用speakPhrase(index, type, rate)，必须添加此函数调用speakWord/speakSentence

## 用户偏好
- 用户非常注重细节，需要反复确认
- 重视历史数据保留
- 要求功能稳定，不再频繁修改
- **"凡是我没有提出改进意见的地方就不要改了"**

## 词汇库统计
- 5年级词汇：460个（vocab_grade5.py）
- 6年级词汇：426个（vocab_grade6.py）
- 总计：886个不重复词汇

## 内容覆盖
- **2026年**：3月31日-12月31日（276天，每天5个词汇）
- **2027年**：1月1日-12月31日（365天，每天5个词汇）
- **总计**：641天内容

## 修复脚本
- `fix_html_files.py`：幂等修复脚本，用于修复HTML文件中的循环按钮和汉语音频问题
- `fix_layout_v2.py`：将循环按钮移到页面顶部
- `fix_memory_batch.py`：批量优化记忆提示
- `fix_memory_tips.py`：完整的英文思维记忆提示字典
- `fix_remaining.py`：修复剩余的记忆提示

## 记忆提示优化（2026-03-30）
- 移除了所有"记住'xxx'的英文表达"废话提示（1493个 → 0个）
- 移除了简单的"xxx=yyy"翻译式提示
- 替换为英文思维记忆法（构词法、谐音、语义关联等）
- 覆盖574个文件，约2000+词汇
