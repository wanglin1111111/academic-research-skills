@echo off
chcp 65001 >nul
echo ================================================
echo    AI原生创作心法工具包 - 一键安装
echo ================================================
echo.

REM 检查OpenClaw是否安装
where openclaw >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到OpenClaw，请先安装OpenClaw
    echo 安装教程：https://openclaw.ai/docs/install
    pause
    exit /b 1
)

REM 获取OpenClaw skills目录
set SKILLS_DIR=%USERPROFILE%\.qclaw\skills
if not exist "%SKILLS_DIR%" (
    mkdir "%SKILLS_DIR%"
)

echo [1/3] 正在安装 ai-native-creation-mindset...
xcopy /E /I /Y "ai-native-creation-mindset" "%SKILLS_DIR%\ai-native-creation-mindset\" >nul
if %errorlevel% equ 0 (
    echo ✅ ai-native-creation-mindset 安装成功
) else (
    echo ❌ ai-native-creation-mindset 安装失败
    pause
    exit /b 1
)

echo.
echo [2/3] 正在安装 ai-creation-prompt-toolkit...
xcopy /E /I /Y "ai-creation-prompt-toolkit" "%SKILLS_DIR%\ai-creation-prompt-toolkit\" >nul
if %errorlevel% equ 0 (
    echo ✅ ai-creation-prompt-toolkit 安装成功
) else (
    echo ❌ ai-creation-prompt-toolkit 安装失败
    pause
    exit /b 1
)

echo.
echo [3/3] 正在验证安装...
if exist "%SKILLS_DIR%\ai-native-creation-mindset\SKILL.md" (
    if exist "%SKILLS_DIR%\ai-creation-prompt-toolkit\SKILL.md" (
        echo ✅ 验证通过，两个技能均已成功安装
    ) else (
        echo ❌ 验证失败：ai-creation-prompt-toolkit 未找到
        pause
        exit /b 1
    )
) else (
    echo ❌ 验证失败：ai-native-creation-mindset 未找到
    pause
    exit /b 1
)

echo.
echo ================================================
echo    🎉 安装完成！
echo ================================================
echo.
echo 下一步：
echo 1. 启动OpenClaw：openclaw gateway start
echo 2. 在对话中说："我想用AI原生创作心法"
echo 3. 阅读技能文档：
echo    - 思维层：%SKILLS_DIR%\ai-native-creation-mindset\SKILL.md
echo    - 执行层：%SKILLS_DIR%\ai-creation-prompt-toolkit\SKILL.md
echo.
echo 文档：
echo    README.md - 完整使用指南
echo    docs\test-report.md - 测试报告
echo.
pause
