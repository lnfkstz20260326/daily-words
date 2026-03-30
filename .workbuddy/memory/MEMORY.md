# 每日英语听说 - 长期记忆

## 项目概述
**每日英语听说** - 一个自动生成每日英语学习页面的Web应用，部署在GitHub Pages上。

## 🔴 2026-03-30 清零重新开始

### 发生了什么
- 今天反复修复汉语音频、按钮功能，始终不稳定
- 用户决定放弃今天成果，清零重来
- 只保留英文内容和记忆提示作为素材库

### 已完成
- **内容备份**：`content_backup/content_backup.json`
  - 641天，3278个单词卡片
  - 每个卡片包含：word_en, phonetic, pos, word_zh, example_en, example_zh, memory_tip
- **清理完成**：删除676个旧文件
- **保留文件**：generate.py, content_backup/, .workbuddy/, backup_before_march29_restore/

## 重要教训

### 为什么3月30日失败
1. **speakPhrase函数缺失** - 按钮调用不存在的函数
2. **循环中断** - cancel()取消了setTimeout中的汉语播放
3. **选择器混乱** - 多个版本的选择器混用
4. **多次修复叠加** - 代码越来越乱

### 核心问题
- Web Speech API的cancel()会中断所有待播放的语音
- setTimeout中的异步播放会被cancel()取消
- 每次修复都引入新问题

## 核心信息

### 访问地址
- GitHub Pages：https://lnfkstz20260326.github.io/daily-words/
- GitHub仓库：https://github.com/lnfkstz20260326/daily-words

### 页面标题
- **首页标题**：📚 每日英语听说
- **首页副标题**：母语化练习，每日随听，明日常新
- **播放界面副标题**：碎片化听说，随时开口交流

### 朗读规则（必须保留！）
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

### 🔴 CSS选择器（HTML使用的类名）
| 功能 | 正确类名 |
|------|----------|
| 卡片 | `.card` |
| 单词英文 | `.word-title` |
| 中文意思 | `.chinese-meaning` |
| 例句英文 | `.example-en` |
| 例句中文 | `.example-cn` |
| 顶部循环按钮 | `.btn-loop` |
| 慢速按钮 | `.btn-slow` |
| 匀速按钮 | `.btn-normal` |
| 常速按钮 | `.btn-fast` |
| 停止按钮 | `.btn-stop` |

### JS字段名对应关系
- phrase.en = 单词/短语本身
- phrase.example = 例句
- phrase.zh = 单词/短语的中文翻译
- phrase.example_zh = 例句的中文翻译

### 技术架构
- **生成器**：generate.py（Python模板）
- **素材库**：content_backup/content_backup.json
- **自动部署**：GitHub Actions（每天早上8点运行）
- **托管**：GitHub Pages

## 用户偏好
- 用户非常注重细节，需要反复确认
- 重视历史数据保留
- 要求功能稳定，不再频繁修改
- **"凡是我没有提出改进意见的地方就不要改了"**
- 内容有价值，功能要稳定

## 下一步计划
1. 创建全新HTML模板（从零写JS，不基于旧代码）
2. JS逻辑要简洁：直接播放，不用setTimeout延迟
3. 先生成一个测试页面验证
4. 确认稳定后再批量生成

## 词汇库统计
- 5年级词汇：460个（vocab_grade5.py）
- 6年级词汇：426个（vocab_grade6.py）
- 总计：886个不重复词汇

## 内容覆盖
- **2026年**：3月31日-12月31日（276天，每天5个词汇）
- **2027年**：1月1日-12月31日（365天，每天5个词汇）
- **总计**：641天内容

## 🔴 2026-03-30 晚 素材库修复

### 问题发现
- 用户反馈2026-04-29有9个词，其中4个重复
- 单词和例句不对应

### 排查结果
- **73个问题**：涉及32个日期
  - 36个例句为空
  - 37个例句与上一个词重复
- **根本原因**：素材库数据本身有错误

### 修复措施
1. 编写 `fix_content_v2.py` 智能修复脚本
2. 去除73个重复词条
3. 用修复后的素材库重新生成641个HTML文件
4. 备份原素材库：`content_backup/content_backup_old.json`

### 修复后验证
2026-04-29 现在正确显示5个词：
- fly → "Birds can fly."
- throw → "Throw the ball."
- catch → "Catch the ball!"
- kick → "Kick the ball."
- hit → "Hit the ball."

### 相关文件
- `content_backup/content_backup.json` - 修复后的素材库
- `content_backup/content_backup_old.json` - 原素材库备份
- `regenerate_html.py` - 重新生成HTML的脚本
- `fix_content_v2.py` - 素材库修复脚本

## 🔴 2026-03-30 夜 轮数显示修复

### 问题
- 轮数显示区域显示 `{currentLoop}/{maxLoops}` 而不是实际数字
- 原因：JS代码使用了模板字符串语法（反引号），可能不被所有浏览器支持

### 修复措施
- 将模板字符串改为字符串拼接方式
- 修改前：`statusDiv.textContent = \`🔄 第 {currentLoop}/{maxLoops} 轮\`;`
- 修改后：`statusDiv.textContent = '🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮';`
- 批量修复了276个HTML文件

### 验证
- 修复后 Line 451: `statusDiv.textContent = '🔄 第 ' + currentLoop + '/' + maxLoops + ' 轮';`

## 🔴 2026-03-30 深夜 记忆小提示清理

### 问题
- 用户反馈"记住xxx的英文表达"这种记忆小提示是废话
- 1433个记忆提示属于这种废话类型

### 修复措施
1. 编写 `fix_memory_tips_simple.py` 清理脚本
2. 128个废话被替换为英语思维提示
3. 1305个废话被删除（留空）
4. 重新生成641个HTML文件

### 英语思维提示示例
- shoes → "Like 'shush' - shoes help you walk quietly"
- dog → "Man's best friend, wags tail"
- apple → "Red and crispy, an apple a day"
- happy → "Smile when you're happy"

### 只修改记忆小提示
- ✅ 未触碰任何功能键
- ✅ 未修改任何JS代码
- ✅ 未修改HTML结构
- ✅ 只清理了记忆小提示内容
