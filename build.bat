@echo off
echo ========================================
echo   悬浮摄像头 - 构建脚本
echo   Windows 7 环境
echo ========================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 创建虚拟环境（可选）
echo [1/3] 安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

:: 安装 PyInstaller
pip install pyinstaller
if errorlevel 1 (
    echo [错误] PyInstaller 安装失败
    pause
    exit /b 1
)

:: 清理旧构建
echo [2/3] 清理旧构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: 打包
echo [3/3] 正在打包...
pyinstaller --onefile --windowed --icon=NONE --name "悬浮摄像头" main.py

if exist dist\悬浮摄像头.exe (
    echo.
    echo ========================================
    echo   构建成功！
    echo   输出文件: dist\悬浮摄像头.exe
    echo ========================================
) else (
    echo.
    echo [错误] 构建失败
)

pause
