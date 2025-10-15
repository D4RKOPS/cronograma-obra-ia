# 🚀 Instrucciones de Instalación - AI Builder Scheduler

## ⚡ Instalación Rápida

### Windows
```bash
# 1. Ejecutar instalación automática
install.bat

# 2. Iniciar la aplicación
start.bat
```

### macOS/Linux
```bash
# 1. Dar permisos de ejecución
chmod +x install.sh start.sh

# 2. Ejecutar instalación automática
./install.sh

# 3. Iniciar la aplicación
./start.sh
```

## 🔧 Instalación Manual

### Prerrequisitos
- **Python 3.7+** (recomendado 3.9+)
- **Node.js 16+** (recomendado 18+)
- **npm** o **yarn**

### 1. Backend (Flask)

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

El backend estará disponible en: `http://localhost:5000`

### 2. Frontend (React)

```bash
# En una nueva terminal, navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar aplicación
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## 🐛 Solución de Problemas

### Error: "Module not found: Error: Can't resolve 'plotly.js-dist-min'"

**Solución**: Este error ya está solucionado. La aplicación ahora usa un componente Gantt personalizado que no depende de Plotly.js.

### Error: "Python no se reconoce como comando"

**Solución**:
1. Instalar Python desde [python.org](https://python.org)
2. Asegurarse de marcar "Add Python to PATH" durante la instalación
3. Reiniciar la terminal

### Error: "npm no se reconoce como comando"

**Solución**:
1. Instalar Node.js desde [nodejs.org](https://nodejs.org)
2. Reiniciar la terminal
3. Verificar instalación: `node --version` y `npm --version`

### Error: "Port 3000 is already in use"

**Solución**:
```bash
# Encontrar proceso usando el puerto
netstat -ano | findstr :3000  # Windows
lsof -i :3000                 # macOS/Linux

# Matar proceso (reemplazar PID con el número del proceso)
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # macOS/Linux
```

### Error: "Port 5000 is already in use"

**Solución**:
```bash
# Encontrar proceso usando el puerto
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Matar proceso
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # macOS/Linux
```

### Error: "Failed to compile"

**Solución**:
1. Limpiar caché de npm:
   ```bash
   cd frontend
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

2. Si persiste, reinstalar dependencias:
   ```bash
   cd frontend
   rm -rf node_modules
   npm install
   ```

### Error: "Module not found" en React

**Solución**:
1. Verificar que todas las dependencias estén instaladas:
   ```bash
   cd frontend
   npm install
   ```

2. Verificar que el archivo existe en la ruta correcta

### Error: "CORS policy"

**Solución**: El backend ya tiene CORS habilitado. Si persiste:
1. Verificar que el backend esté ejecutándose en puerto 5000
2. Verificar que el frontend esté ejecutándose en puerto 3000
3. Reiniciar ambos servicios

## 📋 Verificación de Instalación

### 1. Verificar Backend
```bash
# En el navegador, ir a:
http://localhost:5000

# Deberías ver un JSON con información de la API
```

### 2. Verificar Frontend
```bash
# En el navegador, ir a:
http://localhost:3000

# Deberías ver la interfaz de AI Builder Scheduler
```

### 3. Probar Funcionalidad
1. Ir a `http://localhost:3000`
2. Escribir: "Construir una casa de dos pisos con excavación, cimentación, estructura y acabados"
3. Hacer clic en "Generar Cronograma"
4. Verificar que se genere el cronograma

## 🔄 Actualización

Para actualizar la aplicación:

```bash
# Backend
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

## 📞 Soporte

Si tienes problemas:

1. **Verificar prerrequisitos**: Python 3.7+, Node.js 16+
2. **Revisar logs**: Consola del navegador y terminal
3. **Reiniciar servicios**: Detener y volver a iniciar backend y frontend
4. **Limpiar caché**: `npm cache clean --force`
5. **Reinstalar dependencias**: Borrar `node_modules` y reinstalar

## 🎯 Uso Rápido

Una vez instalado:

1. **Iniciar**: Ejecutar `start.bat` (Windows) o `./start.sh` (macOS/Linux)
2. **Abrir**: Ir a `http://localhost:3000`
3. **Crear proyecto**: Describir tu proyecto o subir archivo CSV
4. **Analizar**: Ver cronograma y estadísticas
5. **Optimizar**: Hacer clic en "Optimizar Cronograma"
6. **Chat**: Hacer preguntas al asistente IA

¡Listo! 🚀
