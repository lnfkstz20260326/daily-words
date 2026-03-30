# 清理脚本 - 删除旧HTML文件，只保留素材库和必要文件
import os
import re
import shutil

# 要保留的文件夹
keep_dirs = ['content_backup', '.workbuddy', '.github', 'github_repo', 'backup_before_march29_restore']

# 要保留的文件
keep_files = ['generate.py', 'vocab_grade5.py', 'vocab_grade6.py', 'extract_content.py']

# 要删除的文件模式
delete_patterns = [
    r'^\d{4}-\d{2}-\d{2}\.html$',  # 日期HTML文件
    r'^fix_.*\.py$',                # 修复脚本
    r'^add_.*\.py$',                # 添加脚本
    r'^restore.*\.py$',             # 恢复脚本
    r'^test.*\.html$',              # 测试文件
    r'^voice-diagnosis\.html$',    # 诊断文件
]

# 统计
deleted_count = 0
kept_count = 0

for filename in os.listdir('.'):
    # 跳过目录
    if os.path.isdir(filename):
        if filename not in keep_dirs:
            print(f'Would delete directory: {filename}/')
        else:
            kept_count += 1
        continue
    
    # 检查是否匹配删除模式
    should_delete = False
    for pattern in delete_patterns:
        if re.match(pattern, filename):
            should_delete = True
            break
    
    # 检查是否在保留列表中
    if filename in keep_files:
        should_delete = False
    
    if should_delete:
        os.remove(filename)
        deleted_count += 1
        print(f'Deleted: {filename}')
    else:
        kept_count += 1

print(f'\nDeleted: {deleted_count} files')
print(f'Kept: {kept_count} files')
print('\nRemaining files:')
for f in sorted(os.listdir('.')):
    if os.path.isdir(f):
        print(f'  [DIR] {f}/')
    else:
        print(f'  {f}')
