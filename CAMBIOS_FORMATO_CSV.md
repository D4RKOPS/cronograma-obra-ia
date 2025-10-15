# 📋 Cambios en el Sistema - Soporte para Nuevos Formatos CSV

## ✅ Cambios Implementados

### 1. **Soporte Mejorado para Formatos CSV**

El sistema ahora puede leer automáticamente diferentes formatos de archivos CSV:

#### **Formato Estándar (Simple)**
```csv
Actividad,Duración,Predecesoras
Excavación,5,
Cimentación,10,Excavación
Estructura,15,Cimentación
```

#### **Formato Extendido (Gestión de Proyectos)**
```csv
Nombre,Und_De_Medida,Cantidad,Rendimiento,Duracion,Comienzo,Fin,codigoPlaneacion
"Torre 01","No Aplica",0,0,"373,84 días","13 julio 2026","15 diciembre 2027",50102010
```

### 2. **Detección Automática de Formato**

El sistema detecta automáticamente el formato del archivo CSV y aplica el procesamiento adecuado:

- **Formato Simple**: Busca columnas `Actividad`, `Duración`, `Predecesoras`
- **Formato Extendido**: Busca columnas `Nombre`, `Duracion`, `Comienzo`, `Fin`
- **Parseo Inteligente**: Maneja comillas anidadas y campos con formato especial

### 3. **Procesamiento de Duraciones**

El sistema ahora puede extraer duraciones en múltiples formatos:

- `"5 días"` → 5 días
- `"10,5 días"` → 11 días (redondeado)
- `"15.3 días"` → 15 días (redondeado)

### 4. **Filtrado Automático**

- Solo procesa actividades con duración mayor a 0
- Ignora filas vacías o con datos inválidos
- Salta actividades sin duración definida

## 🔧 Archivos Modificados

### `ai_builder_scheduler.py`
- ✅ Actualizado `_leer_archivo()` para detectar el formato automáticamente
- ✅ Nuevo método `_procesar_formato_nombre_duracion()` para el formato extendido
- ✅ Nuevo método `_parsear_fila_csv_especial()` para parsear comillas anidadas
- ✅ Mejorado el filtrado de actividades válidas

### `README.md`
- ✅ Agregada sección **"Formatos de Archivo Soportados"**
- ✅ Documentados los dos formatos principales
- ✅ Ejemplos de uso para cada formato

### Archivos Nuevos
- ✅ `ejemplo_cronograma.csv` - Archivo de ejemplo en formato estándar
- ✅ `test_nuevo_csv.py` - Script de prueba para validar la lectura

## 📊 Resultados de Prueba

**Archivo probado:** `Tabla_Tareas1.csv`

```
✅ Formato detectado: Nombre, Duracion, Comienzo, Fin
✅ Actividades encontradas: 717
✅ Duración total: 637 días
✅ Cronograma generado exitosamente
```

## 🚀 Cómo Usar

### Para Usuarios con Archivos Nuevos

1. **Crear un CSV simple:**
   ```csv
   Actividad,Duración,Predecesoras
   Tarea 1,5,
   Tarea 2,10,Tarea 1
   ```

2. **Subir el archivo** a través de la interfaz web o especificar la ruta

3. **El sistema automáticamente:**
   - Detecta el formato
   - Procesa las actividades
   - Genera el cronograma
   - Muestra el diagrama de Gantt

### Para Usuarios con Archivos Exportados

1. **Exportar desde tu software de gestión** (MSProject, Primavera, etc.)

2. **Asegurarse de incluir:**
   - Columna con nombre de actividad
   - Columna con duración en formato "X días"

3. **Subir el archivo** - el sistema lo procesará automáticamente

## 🎯 Ventajas

✅ **Compatibilidad Universal**: Funciona con múltiples formatos
✅ **Detección Automática**: No necesitas configurar nada
✅ **Robusto**: Maneja comillas, espacios y formatos especiales
✅ **Filtrado Inteligente**: Solo procesa datos válidos
✅ **Sin Dependencias**: No requiere predecesoras definidas

## 📝 Notas Técnicas

### Manejo de Comillas Anidadas
El sistema usa un parser personalizado que maneja correctamente CSVs con:
- Comillas dobles escapadas (`""`)
- Campos entre comillas con comas internas
- Múltiples columnas con formatos mixtos

### Extracción de Duraciones
Usa expresiones regulares para extraer duraciones:
```python
r'(\d+(?:[.,]\d+)?)\s*d[ií]as?'
```

Esto captura:
- Números enteros: `5`
- Decimales con punto: `5.3`
- Decimales con coma: `5,3`

### Redondeo
Las duraciones decimales se redondean al entero más cercano:
- `5.3 días` → 5 días
- `5.7 días` → 6 días
- `10,5 días` → 11 días

## 🔄 Compatibilidad con Versión Anterior

✅ **Totalmente compatible**: Los archivos en formato antiguo siguen funcionando
✅ **Sin cambios necesarios**: El código detecta automáticamente el formato
✅ **Backend actualizado**: Flask usa la versión mejorada del scheduler

## 📞 Soporte

Si tienes problemas con un formato específico de CSV:

1. Verifica que tenga columnas de nombre y duración
2. Asegúrate que las duraciones incluyan la palabra "días"
3. Revisa que el archivo esté en codificación UTF-8
4. Usa el archivo `ejemplo_cronograma.csv` como referencia

---

**Actualizado:** Octubre 2025
**Versión:** 2.0

