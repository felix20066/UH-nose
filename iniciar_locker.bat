@echo off
:: =====================================================
::   SCREEN LOCKER EDUCATIVO — Iniciador
::   Doble clic para arrancar. No se necesita nada mas.
:: =====================================================

:: Ir a la carpeta donde esta este .bat
cd /d "%~dp0"

:: --- Verificar si ya somos Administrador ---
net session >nul 2>&1
if %errorlevel% == 0 goto :SOMOS_ADMIN

:: --- No somos admin: relanzar con elevacion ---
echo Solicitando permisos de Administrador...
powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
exit /b

:SOMOS_ADMIN

:: --- Verificar que Python este instalado ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Python no esta instalado o no esta en el PATH.
    echo.
    echo  Descargalo en: https://www.python.org/downloads/
    echo  Al instalar, marca la casilla "Add Python to PATH".
    echo.
    pause
    exit /b
)

:: --- Verificar que el script exista ---
if not exist "%~dp0screen_locker_v3.py" (
    echo.
    echo  [ERROR] No se encontro screen_locker_v3.py
    echo  Asegurate de que este en la misma carpeta que este .bat
    echo.
    pause
    exit /b
)

:: --- Lanzar el locker (sin ventana de consola) ---
start "" pythonw "%~dp0screen_locker_v3.py"
exit
