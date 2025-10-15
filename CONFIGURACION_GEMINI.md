# 🤖 Configuración de Google Gemini AI

Este documento explica cómo configurar Google Gemini AI para mejorar las capacidades del AI Builder Scheduler.

## 📋 Requisitos

- Cuenta de Google
- Acceso a Google AI Studio
- Python 3.7+

## 🔑 Obtener API Key

1. **Visita Google AI Studio:**
   - Ve a: https://makersuite.google.com/app/apikey
   - Inicia sesión con tu cuenta de Google

2. **Crear API Key:**
   - Haz clic en "Create API Key"
   - Copia la clave generada
   - **¡Importante!** Guarda la clave de forma segura

## ⚙️ Configuración

### 1. Crear archivo de configuración

Copia el archivo de ejemplo y configura tu API key:

```bash
cp config.env.example .env
```

### 2. Editar archivo .env

Abre el archivo `.env` y agrega tu API key:

```env
# Configuración de Google Gemini API
GEMINI_API_KEY=tu_api_key_aqui

# Configuración del servidor Flask
FLASK_ENV=development
FLASK_DEBUG=True

# Puerto del servidor
PORT=5000
```

### 3. Instalar dependencias

```bash
# En el directorio backend
pip install -r requirements.txt
```

## 🚀 Funcionalidades con Gemini

Una vez configurado, el sistema tendrá estas capacidades mejoradas:

### 📝 **Análisis Inteligente de Proyectos**
- Extrae actividades, duraciones y dependencias de texto natural
- Comprende contextos complejos de construcción
- Identifica dependencias lógicas automáticamente

### 💬 **Chat Inteligente**
- Responde preguntas complejas sobre cronogramas
- Proporciona explicaciones detalladas
- Sugiere mejoras y optimizaciones

### 🎯 **Optimización con IA**
- Identifica oportunidades de paralelización
- Sugiere reducciones de duración realistas
- Evalúa riesgos de optimizaciones

### ⚠️ **Análisis de Riesgos**
- Identifica riesgos técnicos, climáticos y logísticos
- Evalúa probabilidad e impacto
- Sugiere estrategias de mitigación

## 🔧 Uso en el Código

### Ejemplo básico:

```python
from backend.services.gemini_service import get_gemini_service

# Obtener servicio
gemini_service = get_gemini_service()

if gemini_service:
    # Analizar proyecto
    resultado = gemini_service.analizar_proyecto_construccion(
        "Construcción de casa: Excavación 5 días, Cimentación 10 días después de excavación"
    )
    
    print(resultado['actividades'])
    print(resultado['analisis'])
```

### Endpoints disponibles:

- `POST /api/analyze-risks` - Análisis de riesgos
- `POST /api/ai-optimize` - Optimización con IA

## 🛡️ Seguridad

- **Nunca** subas tu API key al repositorio
- Usa variables de entorno para la configuración
- El archivo `.env` está en `.gitignore`

## 🐛 Solución de Problemas

### Error: "GEMINI_API_KEY no encontrada"
- Verifica que el archivo `.env` existe
- Confirma que la variable `GEMINI_API_KEY` está definida
- Reinicia el servidor después de cambios

### Error: "Gemini no está configurado"
- Verifica que tu API key es válida
- Confirma que tienes acceso a Google AI Studio
- Revisa la conexión a internet

### Error: "Servicio de Gemini no disponible"
- Instala las dependencias: `pip install google-generativeai python-dotenv`
- Verifica que el archivo `backend/services/gemini_service.py` existe

## 📊 Límites y Costos

### Límites gratuitos:
- **60 requests por minuto**
- **1,500 requests por día**
- **32,000 tokens por minuto**

### Costos (después del límite gratuito):
- **$0.0005 por 1K tokens** (entrada)
- **$0.0015 por 1K tokens** (salida)

## 🔄 Fallback

Si Gemini no está disponible, el sistema automáticamente usa:
- Parser regex para texto natural
- Lógica predefinida para respuestas
- Algoritmos básicos de optimización

## 📞 Soporte

Si tienes problemas:
1. Revisa este documento
2. Verifica la configuración
3. Consulta los logs del servidor
4. Contacta al desarrollador

---

**¡Disfruta de las capacidades de IA en tu AI Builder Scheduler!** 🚀
