#!/bin/bash

echo "========================================"
echo "AI Builder Scheduler - Iniciando Servicios"
echo "========================================"

echo ""
echo "[1/3] Iniciando Backend (Flask)..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py &
BACKEND_PID=$!

echo ""
echo "[2/3] Esperando 5 segundos para que el backend se inicie..."
sleep 5

echo ""
echo "[3/3] Iniciando Frontend (React)..."
cd ../frontend
npm install
npm start &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Servicios iniciados correctamente!"
echo "========================================"
echo ""
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Presiona Ctrl+C para detener todos los servicios"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Esperar a que el usuario presione Ctrl+C
wait
