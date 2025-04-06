@echo off
REM 命令顺序：先lupdate后lrelease（第二条命令前需要用户确认）

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

echo.
echo 正在执行 pyside6-rcc...
echo.

pyside6-rcc app/assets/resources.qrc -o app/assets/resources.py

if %ERRORLEVEL% neq 0 (
    echo pyside6-rcc 命令执行失败
    pause
    exit /b 1
)