@echo off
title AutoValue - Car Price Prediction
cd /d "%~dp0"
echo ==========================================
echo       AUTOVALUE CAR PRICE PREDICTION
echo ==========================================
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  %PY% -m venv .venv
)
echo Installing required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if %errorlevel% neq 0 (
  echo Package installation failed. Check your internet connection and Python installation.
  pause
  exit /b 1
)
echo Starting website...
start "" http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
pause
