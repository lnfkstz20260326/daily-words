# -*- coding: utf-8 -*-
"""
修复按钮控制逻辑
1. 删除重复的HTML内容
2. 修复底部导航
3. 优化JS控制逻辑
"""

import os
import glob
import re

def fix_html_file(filepath):
    """修复单个HTML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # =========================================
    # 修复1: 删除重复的卡片内容（第5个卡片的重复）
    # =========================================
    # 匹配 "我需要新衣服" 的重复部分
    duplicate_pattern = r'<div class="example-box">\s*<div class="example-label">例句 Example</div>\s*<div class="example-en">I need new clothes\.</div>\s*<div class="example-cn">我需要新衣服\。</div>\s*</div>\s*<div class="button-group">\s*<button[^>]*>🐢 慢速词×3</button>[^<]*<button[^>]*>🚀 匀速词×3</button>[^<]*<button[^>]*>🐢 慢速句×3</button>[^<]*<button[^>]*>🚀 匀速句×3</button>[^<]*<button[^>]*>⚡ 常速句×3</button>[^<]*<button[^>]*>⏹ 停止</button>\s*</div>\s*</div>\s*'
    
    new_content = re.sub(duplicate_pattern, '', content)
    if new_content != content:
        content = new_content
        modified = True
    
    # =========================================
    # 修复2: 删除重复的loop-status
    # =========================================
    loop_status_pattern = r'<div class="loop-status" id="loopStatus">\s*🔄 点击卡片下方按钮开始朗读 · 页面加载3秒后自动循环播放\s*</div>\s*'
    # 只保留一个
    loop_status_count = len(re.findall(loop_status_pattern, content))
    if loop_status_count > 1:
        content = re.sub(loop_status_pattern, '', content, count=1)
        modified = True
    
    # =========================================
    # 修复3: 删除重复的nav-links
    # =========================================
    nav_links_pattern = r'<div class="nav-links">\s*<a[^>]*>← 前一天</a>\s*<a[^>]*>📅 返回首页</a>\s*<a[^>]*>\s*</div>'
    nav_links_count = len(re.findall(nav_links_pattern, content))
    if nav_links_count > 1:
        content = re.sub(nav_links_pattern, '', content, count=1)
        modified = True
    
    # =========================================
    # 修复4: 修复底部导航（如果有损坏的链接）
    # =========================================
    # 修复 "前一天" 链接 - 应该是前一天而不是 index.html
    # 这个需要根据日期动态计算，但静态文件只能假设一个模式
    # 暂时保持 index.html 作为返回首页
    
    # =========================================
    # 修复5: 优化JS - speakPhrase函数添加循环停止逻辑
    # =========================================
    old_speakPhrase = '''function speakPhrase(index, type, rate) {
            const phrase = phrases[index];
            let text, lang;
            
            if (type === 'word') {
                text = phrase.en;
                lang = 'en-US';
            } else {
                text = phrase.example;
                lang = 'en-US';
            }
            
            window.speechSynthesis.cancel();'''
    
    new_speakPhrase = '''function speakPhrase(index, type, rate) {
            // 点击卡片按钮时，先停止循环播放
            if (isLooping) {
                isLooping = false;
                loopCount = MAX_LOOPS; // 让循环自然结束
                document.getElementById('loopStatus').textContent = '⏹ 已切换到单卡片模式';
            }
            
            const phrase = phrases[index];
            let text, lang;
            
            if (type === 'word') {
                text = phrase.en;
                lang = 'en-US';
            } else {
                text = phrase.example;
                lang = 'en-US';
            }
            
            window.speechSynthesis.cancel();'''
    
    if old_speakPhrase in content:
        content = content.replace(old_speakPhrase, new_speakPhrase)
        modified = True
    
    # =========================================
    # 修复6: 优化 stopSpeaking 函数
    # =========================================
    old_stopSpeaking = '''function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = 0;
            document.getElementById('loopStatus').textContent = '⏹ 已停止';
            document.getElementById('loopBtn').textContent = '▶️ 开始循环朗读';
        }'''
    
    new_stopSpeaking = '''function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            document.getElementById('loopStatus').textContent = '⏹ 已停止';
            document.getElementById('loopBtn').textContent = '▶️ 开始循环朗读';
        }'''
    
    if old_stopSpeaking in content and new_stopSpeaking not in content:
        content = content.replace(old_stopSpeaking, new_stopSpeaking)
        modified = True
    
    # =========================================
    # 修复7: 优化 goBack 函数
    # =========================================
    old_goBack = '''function goBack() {
    window.speechSynthesis.cancel();
    isLooping = false;
    loopCount = 0;
    if (document.getElementById('loopStatus')) {
        document.getElementById('loopStatus').textContent = '⏹ 已停止';
    }
    if (document.getElementById('loopBtn')) {
        document.getElementById('loopBtn').textContent = '▶️ 开始循环朗读';
    }
    window.location.href = 'index.html';
}'''
    
    new_goBack = '''function goBack() {
    window.speechSynthesis.cancel();
    isLooping = false;
    loopCount = MAX_LOOPS;
    const statusEl = document.getElementById('loopStatus');
    const btnEl = document.getElementById('loopBtn');
    if (statusEl) statusEl.textContent = '⏹ 已停止';
    if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
    window.location.href = 'index.html';
}'''
    
    if old_goBack in content:
        content = content.replace(old_goBack, new_goBack)
        modified = True
    
    # 修复重复的goBack函数定义
    if content.count('function goBack()') > 1:
        # 删除多余的 goBack 函数定义（保留第一个）
        pattern = r'(function goBack\(\) \{[^}]+\})\s*(function goBack\(\) \{[^}]+\})'
        match = re.search(pattern, content)
        if match:
            content = content.replace(match.group(0), match.group(1))
            modified = True
    
    # =========================================
    # 修复8: 确保只有一个底部导航
    # =========================================
    nav_pattern = r'(<div class="nav-links">\s*<a[^>]*>← 前一天</a>\s*<a[^>]*>📅 返回首页</a>\s*</div>)'
    nav_matches = list(re.finditer(nav_pattern, content))
    if len(nav_matches) > 1:
        # 删除多余的导航
        for i in range(len(nav_matches) - 1, 0, -1):
            start = nav_matches[i].start()
            end = nav_matches[i].end()
            content = content[:start] + content[end:]
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return modified


def main():
    # 设置控制台编码
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 获取所有HTML文件
    html_files = glob.glob('2026-*.html') + glob.glob('2027-*.html')
    html_files.sort()
    
    fixed_count = 0
    for filepath in html_files:
        if fix_html_file(filepath):
            fixed_count += 1
            print(f"[OK] {filepath}")
    
    print(f"\nTotal: Fixed {fixed_count} files")


if __name__ == '__main__':
    main()
