@echo off
REM 激活Python虚拟环境并执行PySide6命令的bat脚本
REM 命令顺序：先lupdate后lrelease（第二条命令前需要用户确认）

REM 设置虚拟环境路径（根据你的实际路径修改）
set VENV_ACTIVATE=.\Scripts\activate.bat

REM 检查虚拟环境是否存在
if not exist "%VENV_ACTIVATE%" (
    echo 错误：找不到虚拟环境脚本 %VENV_ACTIVATE%
    echo 请确保PySide6虚拟环境存在于当前目录下
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 正在激活 PySide6 虚拟环境...
echo.
call "%VENV_ACTIVATE%"

if %ERRORLEVEL% neq 0 (
    echo 激活虚拟环境失败
    pause
    exit /b 1
)

echo 正在执行 pyside6-lupdate...
echo.
pyside6-lupdate main.py app/home_interface.py app/setting_interface.py -ts app/assets/language/translation_zh_CN.ts

if %ERRORLEVEL% neq 0 (
    echo pyside6-lupdate 命令执行失败
    pause
    exit /b 1
)

echo.
set /p =请在ts文件翻译完成后按回车键执行 pyside6-lrelease...<nul
pause >nul
echo.
echo 正在执行 pyside6-lrelease...
echo.

pyside6-lrelease app/assets/language/translation_zh_CN.ts -qm app/assets/language/translation_zh_CN.qm

if %ERRORLEVEL% neq 0 (
    echo pyside6-lrelease 命令执行失败
    pause
    exit /b 1
)