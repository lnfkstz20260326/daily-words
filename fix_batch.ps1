# PowerShell批量修复脚本
$files = Get-ChildItem -Filter "202*.html"
$fixed = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw

    # 修复1: 移动top-controls到正确位置
    # 找到header结束和第一个card之间的位置

    # 删除错误位置的top-controls (在第一个card之后)
    $pattern1 = '(</div>\s*<div class="top-controls">.*?</div>\s*\s*\s*<div class="card">)'
    if ($content -match $pattern1) {
        $content = $content -replace $pattern1, '$1'
    }

    # 在header后添加top-controls
    $pattern2 = '(<div class="grade">.*?</div>\s*</div>\s*)'
    $replacement2 = @'
$1
        <div class="top-controls">
            <button class="btn btn-loop" id="loopBtn" onclick="toggleLoop()">
                ▶️ 开始循环朗读
            </button>
            <button class="btn btn-secondary" onclick="goBack()">
                ⬅️ 返回选择
            </button>
        </div>
'@

    if ($content -notmatch 'top-controls' -or $content -match '\s+<div class="card">\s*<div class="top-controls">') {
        $content = $content -replace $pattern2, $replacement2
    }

    # 修复2: 添加top-controls样式
    if ($content -notmatch '\.top-controls \{') {
        $content = $content -replace '(\.card \{)', @'
        .top-controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

$1
'@
    }

    # 修复3: 添加btn-secondary样式
    if ($content -notmatch '\.btn-secondary \{') {
        $content = $content -replace '(\.btn-loop \{[^}]+\})', @'
$1
        .btn-secondary {
            background: linear-gradient(135deg, #764ba2 0%, #6a3093 100%);
            color: white;
        }
'@
    }

    # 修复4: speakPhrase函数 - 添加循环停止逻辑
    $oldSpeakPhrase = @'
function speakPhrase(index, type, rate) {
            const phrase = phrases[index];
            let text, lang;

            if (type === 'word') {
'@

    $newSpeakPhrase = @'
function speakPhrase(index, type, rate) {
            // 点击卡片按钮时，先停止循环播放
            if (isLooping) {
                isLooping = false;
                loopCount = MAX_LOOPS;
                const statusEl = document.getElementById('loopStatus');
                if (statusEl) statusEl.textContent = '⏹ 已切换到单卡片模式';
            }

            const phrase = phrases[index];
            let text, lang;

            if (type === 'word') {
'@

    if ($content -match [regex]::Escape($oldSpeakPhrase) -and $content -notmatch '// 点击卡片按钮时，先停止循环播放') {
        $content = $content -replace [regex]::Escape($oldSpeakPhrase), $newSpeakPhrase
    }

    # 修复5: stopSpeaking函数
    $oldStop = @'
function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = 0;
            document.getElementById('loopStatus').textContent = '⏹ 已停止';
        }
'@

    $newStop = @'
function stopSpeaking() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            const statusEl = document.getElementById('loopStatus');
            const btnEl = document.getElementById('loopBtn');
            if (statusEl) statusEl.textContent = '⏹ 已停止';
            if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
        }
'@

    if ($content -match 'function stopSpeaking\(\)' -and $content -notmatch 'loopCount = MAX_LOOPS;') {
        $content = $content -replace [regex]::Escape($oldStop), $newStop
    }

    # 修复6: goBack函数
    $oldGoBack = 'function goBack\(\) \{[^}]+window\.location\.href = .index\.html.;[^}]+\}'

    $newGoBack = @'
function goBack() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            const statusEl = document.getElementById('loopStatus');
            const btnEl = document.getElementById('loopBtn');
            if (statusEl) statusEl.textContent = '⏹ 已停止';
            if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
            window.location.href = 'index.html';
        }
'@

    if ($content -match 'function goBack\(\)' -and $content -notmatch 'const statusEl = document\.getElementById\(\'loopStatus\'\)') {
        $content = $content -replace $oldGoBack, $newGoBack
    }

    # 修复7: 添加goBack函数（如果没有）
    if ($content -notmatch 'function goBack\(\)') {
        $oldStopPattern = 'function stopSpeaking\(\) \{[^}]+\}[^}]+\}'
        $goBackFunc = @'

        function goBack() {
            window.speechSynthesis.cancel();
            isLooping = false;
            loopCount = MAX_LOOPS;
            const statusEl = document.getElementById('loopStatus');
            const btnEl = document.getElementById('loopBtn');
            if (statusEl) statusEl.textContent = '⏹ 已停止';
            if (btnEl) btnEl.textContent = '▶️ 开始循环朗读';
            window.location.href = 'index.html';
        }
'@
        if ($content -match 'function stopSpeaking\(\)') {
            $content = $content -replace '(function stopSpeaking\(\) \{[^}]+\})', "`$1$goBackFunc"
        }
    }

    Set-Content -Path $file.FullName -Value $content -NoNewline
    $fixed++
    Write-Host "[OK] $($file.Name)"
}

Write-Host ""
Write-Host "Total: Fixed $fixed files"
