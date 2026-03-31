@echo off
if not exist venv (
    py -m venv venv
)
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo Servidor Flask: http://127.0.0.1:5000
py app.py
pause
