# 🚀 Guía Rápida - AI Builder Scheduler

## ✅ Lo que se ha actualizado

### 1. **Soporte para múltiples formatos de CSV**
- ✅ Formato estándar (Actividad, Duración, Predecesoras)
- ✅ Formato extendido (Nombre, Duracion, Comienzo, Fin)
- ✅ Detección automática del formato
- ✅ Extracción de fecha de inicio del archivo CSV

### 2. **Detección de fecha inicial**
- El sistema ahora **detecta automáticamente** la fecha de inicio del archivo CSV
- Si el CSV tiene fechas (columna "Comienzo"), usa la primera fecha válida
- Si no tiene fechas, usa la fecha actual del sistema

## 📁 Cómo usar el nuevo formato

### Opción A: Archivo CSV Estándar (Simple)

Crea un archivo CSV con estas columnas:

```csv
Actividad,Duración,Predecesoras
Excavación,5,
Cimentación,10,Excavación
Estructura,15,Cimentación
Muros,8,Estructura
```

### Opción B: Archivo desde Software de Gestión

Si exportas desde MS Project, Primavera u otro software, el sistema lo detectará automáticamente:

```csv
Nombre,Und_De_Medida,Cantidad,Rendimiento,Duracion,Comienzo,Fin,codigoPlaneacion
"Torre 01","No Aplica",0,0,"374 días","13 julio 2026 7:00 a. m.","22 octubre 2026",50102010
"Cimentación","Metro Cubico",94,7,"14 días","25 julio 2026 8:30 a. m.","14 agosto 2026",5010201015
```

**Importante:** 
- El sistema solo necesita las columnas `Nombre` y `Duracion`
- Las demás columnas son opcionales
- La duración debe incluir la palabra "días"

## 🖥️ Cómo iniciar el sistema

### Backend (Flask)

```bash
cd backend
python app.py
```

El backend estará disponible en: `http://localhost:5000`

### Frontend (React)

En otra terminal:

```bash
cd frontend
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## 📤 Cómo subir tu archivo CSV

### Desde la Interfaz Web:

1. Abre `http://localhost:3000`
2. Haz clic en "Nuevo Proyecto"
3. Arrastra tu archivo CSV o haz clic para seleccionarlo
4. Espera a que se procese
5. ¡Listo! Verás tu cronograma en formato Gantt

### Desde Python directamente:

```python
from ai_builder_scheduler import AIBuilderScheduler

scheduler = AIBuilderScheduler()

# Leer tu archivo CSV
df = scheduler.leer_entrada("Tabla_Tareas1.csv")

# Generar cronograma
cronograma = scheduler.generar_cronograma(df)

# Mostrar diagrama de Gantt
scheduler.mostrar_gantt(cronograma)
```

## 🧪 Cómo probar que todo funciona

### Prueba 1: Leer el CSV

```bash
python test_nuevo_csv.py
```

Esto debería mostrar:
- ✅ Archivo procesado: 717 actividades
- ✅ Fecha de inicio: 11/11/2025 (detectada del CSV)
- ✅ Cronograma generado exitosamente

### Prueba 2: Backend completo

```bash
python test_backend_upload.py
```

**Nota:** Asegúrate de que el backend esté corriendo primero.

### Prueba 3: Integración completa

```bash
python test_integracion_csv.py
```

Esto prueba:
- ✅ Formato estándar
- ✅ Formato extendido
- ✅ Entrada de texto natural

## 📊 Ejemplo de salida esperada

Cuando subes `Tabla_Tareas1.csv`:

```
Detectado formato con columnas Nombre, Duracion, Comienzo, Fin...
Fecha de inicio detectada del archivo: 2025-11-11
Archivo procesado: 717 actividades encontradas

Total actividades: 717
Duración total: 637 días
Fecha inicio: 11/11/2025
Fecha fin: 10/08/2027
```

## ❓ Preguntas Frecuentes

### ¿Qué pasa si mi CSV no tiene fechas?

No hay problema. El sistema usará la fecha actual como inicio y calculará las demás fechas automáticamente.

### ¿Qué pasa si mi CSV tiene un formato diferente?

El sistema intenta detectar automáticamente el formato. Si no funciona, crea un CSV con el formato estándar:

```csv
Actividad,Duración,Predecesoras
Tu actividad,10,
```

### ¿Puedo cambiar la fecha de inicio?

Sí, desde Python:

```python
scheduler = AIBuilderScheduler()
scheduler.configurar_fecha_inicio("2026-01-01")  # YYYY-MM-DD
```

### ¿El sistema maneja dependencias?

Sí, si tu CSV tiene la columna `Predecesoras`:

```csv
Actividad,Duración,Predecesoras
Tarea A,5,
Tarea B,10,Tarea A
Tarea C,8,"Tarea A,Tarea B"
```

### Mi archivo tiene muchas actividades, ¿hay límite?

No hay límite específico. El sistema probado con:
- ✅ 717 actividades (Tabla_Tareas1.csv)
- ✅ Procesamiento en segundos
- ✅ Generación de cronograma completo

## 🎯 Características principales

### 1. Detección Automática
- El sistema detecta el formato del CSV automáticamente
- No necesitas configurar nada

### 2. Fecha de Inicio Inteligente
- Si el CSV tiene fechas, las usa
- Si no, usa la fecha actual

### 3. Filtrado Automático
- Solo procesa actividades con duración > 0
- Ignora filas vacías o inválidas

### 4. Formatos de Duración
- `"5 días"` → 5 días
- `"10,5 días"` → 11 días (redondeado)
- `"15.3 días"` → 15 días (redondeado)

## 📞 Solución de problemas

### El backend no inicia

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### El frontend no inicia

```bash
cd frontend
npm install
npm start
```

### Error al leer el CSV

Verifica que:
1. El archivo esté en formato UTF-8
2. Tenga al menos una columna con nombre de actividad
3. Tenga una columna con duración en formato "X días"

### La fecha no se detecta

Si el CSV tiene fechas pero no se detectan:
- Verifica que estén en formato: "DD mes YYYY H:MM a./p. m."
- Ejemplo: "11 noviembre 2025 7:00 a. m."

## 📚 Archivos de referencia

- `ejemplo_cronograma.csv` - Ejemplo de formato estándar
- `Tabla_Tareas1.csv` - Ejemplo de formato extendido (real)
- `CAMBIOS_FORMATO_CSV.md` - Documentación técnica de cambios
- `README.md` - Documentación completa

## 🎉 ¡Listo!

Ahora puedes:
1. ✅ Subir archivos CSV en múltiples formatos
2. ✅ El sistema detecta automáticamente el formato
3. ✅ Extrae la fecha de inicio del archivo
4. ✅ Genera cronogramas completos con Gantt
5. ✅ Optimiza automáticamente el proyecto

---

**Actualizado:** Octubre 2025  
**Versión:** 2.0

