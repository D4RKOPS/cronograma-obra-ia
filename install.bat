@echo off
echo ========================================
echo AI Builder Scheduler - Instalacion
echo ========================================

echo.
echo [1/3] Instalando dependencias del Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Backend instalado correctamente!

echo.
echo [2/3] Instalando dependencias del Frontend...
cd ..\frontend
npm install
echo Frontend instalado correctamente!

echo.
echo [3/3] Instalacion completada!
echo ========================================
echo.
echo Para iniciar la aplicacion, ejecuta:
echo   start.bat
echo.
echo O manualmente:
echo   Backend: cd backend && venv\Scripts\activate && python app.py
echo   Frontend: cd frontend && npm start
echo.
pause
