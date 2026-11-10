@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creation de l'environnement virtuel...
    python -m venv .venv || goto :error
)

call ".venv\Scripts\activate.bat"
python -m pip install --disable-pip-version-check -q -r requirements.txt || goto :error
python main.py %*
goto :eof

:error
echo.
echo Une erreur est survenue. Verifiez que Python 3.10+ est installe et dans le PATH.
pause
exit /b 1
