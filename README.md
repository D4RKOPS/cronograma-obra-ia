# 🏗️ AI Builder Scheduler - Interfaz Web

> **🆕 ACTUALIZACIÓN v2.0** - Ahora con soporte para múltiples formatos de CSV y detección automática de fechas

**Asistente Inteligente para Cronogramas de Construcción con Interfaz Web Moderna**

Una aplicación web completa con React y Flask que permite generar, analizar y optimizar cronogramas de proyectos de construcción usando inteligencia artificial.

---

## 🎊 Novedades de la Versión 2.0

✅ **Soporte Multi-Formato CSV**: Lee automáticamente diferentes formatos de archivos  
✅ **Detección de Fechas**: Extrae la fecha de inicio del archivo CSV automáticamente  
✅ **Parser Mejorado**: Maneja comillas anidadas y formatos complejos  
✅ **Frontend Actualizado**: Nueva interfaz que muestra los formatos soportados  
✅ **Probado con 717 actividades**: Funcionamiento verificado con proyectos reales

📖 **[Ver Guía Rápida](GUIA_RAPIDA.md)** | **[Cambios Detallados](CAMBIOS_FORMATO_CSV.md)**

---

## 🎯 Características

### 🌐 **Interfaz Web Moderna**
- **Diseño Responsivo**: Funciona perfectamente en desktop, tablet y móvil
- **UI/UX Profesional**: Interfaz moderna con gradientes, animaciones y efectos glass
- **Navegación Intuitiva**: Menú de navegación claro y fácil de usar
- **Tema Atractivo**: Colores modernos y tipografía profesional

### 🤖 **Funcionalidades de IA**
- **Procesamiento de Lenguaje Natural**: Describe tu proyecto en español
- **Carga de Archivos**: Soporte para CSV, XLS, XLSX
- **Chat Interactivo**: Conversa con el asistente IA
- **Optimización Automática**: Reduce tiempos y mejora eficiencia
- **Análisis Inteligente**: Responde preguntas sobre el proyecto
- **🧠 Google Gemini AI**: Análisis avanzado con IA real
- **⚠️ Análisis de Riesgos**: Identificación automática de riesgos
- **🎯 Optimización con IA**: Mejoras inteligentes del cronograma

### 📊 **Visualización Avanzada**
- **Diagramas de Gantt Interactivos**: Usando Plotly.js
- **Resumen del Proyecto**: Estadísticas y métricas clave
- **Timeline Visual**: Representación gráfica del cronograma
- **Indicadores de Optimización**: Muestra mejoras aplicadas

## 🚀 Instalación y Configuración

### 🤖 Configuración de Google Gemini AI (Opcional)

Para habilitar las funcionalidades avanzadas de IA:

1. **Obtén tu API Key:**
   - Ve a: https://makersuite.google.com/app/apikey
   - Crea una API key gratuita

2. **Configura el archivo .env:**
   ```bash
   cp config.env.example .env
   # Edita .env y agrega tu API key
   ```

3. **Instala dependencias adicionales:**
   ```bash
   pip install google-generativeai python-dotenv
   ```

📖 **Documentación completa:** [CONFIGURACION_GEMINI.md](CONFIGURACION_GEMINI.md)

### Prerrequisitos
- Python 3.7+
- Node.js 16+
- npm o yarn

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd Generaci-n-y-Optimizacion-de-un-Cronograma-de-Obra-con-Inteligencia-Artificial
```

### 2. Configurar Backend (Flask)
```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

El backend estará disponible en: `http://localhost:5000`

### 3. Configurar Frontend (React)
```bash
# En una nueva terminal, navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar aplicación
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## 🎨 Capturas de Pantalla

### Página Principal
- Interfaz de bienvenida con opciones de entrada
- Diseño moderno con gradientes y efectos glass
- Opciones para texto natural o carga de archivos

### Cronograma Generado
- Diagrama de Gantt interactivo
- Resumen del proyecto con estadísticas
- Botón de optimización prominente

### Chat con IA
- Interfaz de chat moderna
- Preguntas rápidas predefinidas
- Respuestas contextuales del asistente

## 📱 Uso de la Aplicación

### 1. **Crear Nuevo Proyecto**
- **Opción A**: Describe tu proyecto en lenguaje natural
  ```
  "Construir una casa de dos pisos con excavación, cimentación, estructura y acabados."
  ```
- **Opción B**: Sube un archivo CSV/Excel con las actividades

### 2. **Analizar Cronograma**
- Visualiza el diagrama de Gantt generado
- Revisa las estadísticas del proyecto
- Explora las fechas de inicio y fin

### 3. **Optimizar Proyecto**
- Haz clic en "Optimizar Cronograma"
- Ve las mejoras aplicadas automáticamente
- Compara duraciones antes y después

### 4. **Chat con el Asistente**
- Haz preguntas sobre el proyecto
- Usa las preguntas rápidas predefinidas
- Obtén análisis detallados del cronograma

## 🔧 Estructura del Proyecto

```
AI-Builder-Scheduler/
├── backend/
│   ├── app.py                 # API Flask
│   ├── requirements.txt       # Dependencias Python
│   └── uploads/              # Archivos temporales
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML principal
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── ChatInterface.js
│   │   │   ├── GanttChart.js
│   │   │   ├── FileUpload.js
│   │   │   └── ProjectSummary.js
│   │   ├── services/
│   │   │   └── api.js        # Servicios API
│   │   ├── App.js            # Componente principal
│   │   ├── index.js          # Punto de entrada
│   │   └── index.css         # Estilos globales
│   ├── package.json          # Dependencias Node.js
│   ├── tailwind.config.js    # Configuración Tailwind
│   └── postcss.config.js     # Configuración PostCSS
├── ai_builder_scheduler.py   # Lógica principal de IA
└── README.md                 # Documentación
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask**: Framework web Python
- **Flask-CORS**: Manejo de CORS
- **Pandas**: Manipulación de datos
- **Plotly**: Generación de gráficos

### Frontend
- **React 18**: Framework de UI
- **Tailwind CSS**: Framework de estilos
- **Plotly.js**: Visualización de gráficos
- **Axios**: Cliente HTTP
- **React Dropzone**: Carga de archivos
- **Lucide React**: Iconos modernos

## 📊 API Endpoints

### `POST /api/process`
Procesa entrada del usuario (texto o archivo)
```json
{
  "input": "texto del proyecto",
  "type": "text"
}
```

### `POST /api/optimize`
Optimiza el cronograma actual

### `POST /api/chat`
Envía mensaje al chat
```json
{
  "question": "¿Cuánto dura el proyecto?"
}
```

### `POST /api/upload`
Carga archivo CSV/Excel

### `GET /api/status`
Obtiene estado del sistema

## 🎯 Ejemplos de Uso

### Proyecto de Casa
```
"Construir una casa de dos pisos con excavación, cimentación, estructura, muros, techos, instalaciones y acabados."
```

### Proyecto de Edificio
```
"Construir un edificio de oficinas de 5 pisos con cimentación profunda, estructura de concreto, fachada de vidrio y acabados interiores."
```

### Preguntas al Chat
- "¿Cuánto dura el proyecto?"
- "¿Qué tareas puedo hacer en paralelo?"
- "¿Cuál es la ruta crítica?"
- "Optimiza el cronograma"
- "¿Cuáles son las dependencias?"

## 📁 Formatos de Archivo Soportados

El sistema puede leer archivos CSV y Excel en diferentes formatos:

### Formato 1: Estándar (Actividad, Duración, Predecesoras)
El formato más simple y recomendado para nuevos proyectos:

```csv
Actividad,Duración,Predecesoras
Excavación,5,
Cimentación,10,Excavación
Estructura,15,Cimentación
Muros,8,Estructura
```

**Columnas:**
- `Actividad`: Nombre de la actividad o tarea
- `Duración`: Duración en días (número entero)
- `Predecesoras`: Actividades que deben completarse antes (opcional)

### Formato 2: Extendido (Nombre, Duración, Comienzo, Fin)
Para archivos exportados de software de gestión de proyectos:

```csv
Nombre,Und_De_Medida,Cantidad,Rendimiento,Duracion,Comienzo,Fin,codigoPlaneacion
"Torre 01","No Aplica",0,0,"373,84 días","13 julio 2026 7:00 a. m.","15 diciembre 2027 3:34 p. m.",50102010
"Cimentación","Metro Cubico",94,7,"14 días","25 julio 2026 8:30 a. m.","14 agosto 2026 8:30 a. m.",5010201015
```

**Columnas requeridas:**
- `Nombre`: Nombre de la actividad
- `Duracion`: Duración en formato "X días" o "X,Y días"

El sistema detecta automáticamente el formato y procesa las actividades con duración mayor a 0.

### Formatos de Duración Soportados:
- `"5 días"`
- `"10,5 días"`
- `"15.3 días"`

**Nota:** El sistema solo procesa actividades con duración válida (mayor a 0 días).

## 🔧 Personalización

### Agregar Nuevos Tipos de Actividades
Edita `ai_builder_scheduler.py`:
```python
self.patrones_actividades = {
    'tu_actividad': ['patrón1', 'patrón2'],
    # ...
}
```

### Modificar Estilos
Edita `frontend/src/index.css` o usa las clases de Tailwind CSS.

### Configurar API
Modifica `frontend/src/services/api.js` para cambiar la URL del backend.

## 🚀 Despliegue

### Backend (Heroku, Railway, etc.)
```bash
# Crear Procfile
echo "web: python app.py" > Procfile

# Configurar variables de entorno
export FLASK_ENV=production
```

### Frontend (Netlify, Vercel, etc.)
```bash
# Build de producción
npm run build

# Subir carpeta build/
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Algunas ideas:

- **Nuevas funcionalidades**: Análisis de recursos, costos, etc.
- **Mejoras de UI**: Nuevos componentes, animaciones
- **Optimizaciones**: Algoritmos más avanzados
- **Integraciones**: APIs externas, calendarios
- **Internacionalización**: Soporte para más idiomas

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🆘 Soporte

Si tienes problemas:

1. **Verifica las dependencias**: Asegúrate de tener Python 3.7+ y Node.js 16+
2. **Revisa los logs**: Mira la consola del navegador y terminal
3. **Reinicia los servicios**: Detén y vuelve a iniciar backend y frontend
4. **Limpia caché**: `npm run build` y borra node_modules si es necesario

---

**¡Construye el futuro con IA! 🚀**

*Una aplicación web moderna para la gestión inteligente de cronogramas de construcción.*