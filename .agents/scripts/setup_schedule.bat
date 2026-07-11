@echo off
chcp 65001 >nul
echo ========================================
echo  超级个体知识库 - 自动脚本安装
echo ========================================
echo.

set PYTHON=C:\Users\quand\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
set SCRIPT_DIR=E:\超级个体知识库\.agents\scripts

echo 1/2 安装每日早报 (每天 08:00)
schtasks /create /tn "SuperDB_DailyBrief" /tr "%PYTHON% %SCRIPT_DIR%\daily_brief.py" /sc daily /st 08:00 /f
echo.

echo 2/2 安装周报 (每周日 20:00)
schtasks /create /tn "SuperDB_WeeklyReport" /tr "%PYTHON% %SCRIPT_DIR%\weekly_report.py" /sc weekly /d SUN /st 20:00 /f
echo.

echo ========================================
echo 安装完成!
echo.
echo 任务列表:
echo   SuperDB_DailyBrief    - 每天 08:00 生成早报
echo   SuperDB_WeeklyReport  - 每周日 20:00 生成周报
echo.
echo 如果失败，以管理员身份重新运行此文件。
echo ========================================
pause
