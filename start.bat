@echo off
echo ========================================
echo AI Builder Scheduler - Iniciando Servicios
echo ========================================

echo.
echo [1/3] Iniciando Backend (Flask)...
cd backend
start "Backend Flask" cmd /k "python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python app.py"

echo.
echo [2/3] Esperando 5 segundos para que el backend se inicie...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] Iniciando Frontend (React)...
cd ..\frontend
start "Frontend React" cmd /k "npm install && npm start"

echo.
echo ========================================
echo Servicios iniciados correctamente!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar...
pause > nul
