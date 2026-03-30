# -*- coding: utf-8 -*-
"""
修复脚本 v2 - 修复循环按钮位置和记忆提示
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
    # 修复1: 把底部循环按钮移到顶部
    # =========================================
    
    # 找到header结束位置，在其后添加顶部控制按钮
    header_pattern = r'(<div class="header">.*?</div>\s*)'
    header_match = re.search(header_pattern, content, re.DOTALL)
    
    if header_match:
        header_end = header_match.end()
        
        # 新的顶部控制区域HTML
        top_controls = '''
        <div class="top-controls">
            <button class="btn btn-loop" id="loopBtn" onclick="toggleLoop()">
                ▶️ 开始循环朗读
            </button>
            <button class="btn btn-secondary" onclick="goBack()">
                ⬅️ 返回选择
            </button>
        </div>

        '''
        
        # 检查是否已有top-controls
        if 'class="top-controls"' not in content:
            content = content[:header_end] + '\n' + top_controls + content[header_end:]
            modified = True
    
    # =========================================
    # 修复2: 删除底部的循环按钮（如果有的话）
    # =========================================
    
    # 删除底部的循环按钮区域（多个换行+button-group）
    bottom_loop_pattern = r'\s*<div class="button-group"\s+style="justify-content:\s*center;\s*margin-bottom:\s*20px;">\s*<button class="btn btn-loop"\s+id="loopBtn"\s+onclick="toggleLoop\(\)">\s*▶️ 开始循环朗读\s*</button>\s*</div>\s*'
    new_content = re.sub(bottom_loop_pattern, '\n', content)
    
    if new_content != content:
        content = new_content
        modified = True
    
    # =========================================
    # 修复3: 添加goBack函数
    # =========================================
    
    if 'function goBack()' not in content:
        # 在stopSpeaking函数附近添加goBack函数
        stop_pattern = r'(function stopSpeaking\(\)\s*\{[^}]+\})'
        stop_match = re.search(stop_pattern, content, re.DOTALL)
        
        if stop_match:
            stop_func = stop_match.group(1)
            goback_func = '''
function goBack() {
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
}
            
            '''
            content = content.replace(stop_func, stop_func + '\n' + goback_func)
            modified = True
    
    # =========================================
    # 修复4: 添加top-controls样式
    # =========================================
    
    if '.top-controls' not in content:
        # 在CSS中添加top-controls样式
        header_style_pattern = r'(\.header\s*\{[^}]+\})'
        header_match = re.search(header_style_pattern, content, re.DOTALL)
        
        if header_match:
            header_style = header_match.group(1)
            new_style = header_style + '''
        .top-controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
'''
            content = content.replace(header_style, new_style)
            modified = True
    
    # =========================================
    # 修复5: 添加.btn-secondary样式
    # =========================================
    
    if '.btn-secondary' not in content:
        # 在btn-loop样式后添加secondary样式
        btn_loop_pattern = r'(\.btn-loop\s*\{[^}]+\})'
        btn_loop_match = re.search(btn_loop_pattern, content, re.DOTALL)
        
        if btn_loop_match:
            btn_loop_style = btn_loop_match.group(1)
            new_style = btn_loop_style + '''
        .btn-secondary {
            background: linear-gradient(135deg, #764ba2 0%, #6a3093 100%);
            color: white;
        }
'''
            content = content.replace(btn_loop_style, new_style)
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
        else:
            print(f"[--] {filepath}")
    
    print(f"\nTotal: Fixed {fixed_count} files")


if __name__ == '__main__':
    main()
