#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Builder Scheduler - Asistente Inteligente para Cronogramas de Construcción
================================================================================

Este módulo implementa un asistente de IA que puede generar, analizar y optimizar
cronogramas de proyectos de construcción (diagramas de Gantt) a partir de entrada
en lenguaje natural o archivos CSV/Excel.

Autor: AI Assistant
Versión: 1.0
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
import os
import sys
from typing import Dict, List, Tuple, Optional, Union

# Importar servicio de Gemini
try:
    from backend.services.gemini_service import get_gemini_service
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Gemini no disponible - usando lógica predefinida")


class AIBuilderScheduler:
    """
    Clase principal que maneja la generación y optimización de cronogramas de construcción.
    
    Esta clase proporciona métodos para:
    - Procesar entrada en lenguaje natural o archivos CSV
    - Generar cronogramas con dependencias
    - Visualizar diagramas de Gantt interactivos
    - Optimizar cronogramas automáticamente
    - Responder preguntas sobre el proyecto
    """
    
    def __init__(self, fecha_inicio=None):
        """Inicializa el scheduler con configuraciones por defecto."""
        self.df_actividades = None
        self.fecha_inicio = fecha_inicio if fecha_inicio else datetime.now().date()
        self.conversacion_activa = True
        
        # Patrones para extraer información de texto natural
        self.patrones_actividades = {
            'excavacion': ['excavación', 'excavar', 'excavado', 'movimiento de tierras'],
            'cimentacion': ['cimentación', 'cimientos', 'fundación', 'fundaciones'],
            'estructura': ['estructura', 'estructuras', 'columnas', 'vigas', 'losas'],
            'muros': ['muros', 'paredes', 'tabiques', 'albañilería'],
            'techos': ['techo', 'techos', 'cubierta', 'cubiertas'],
            'instalaciones': ['instalaciones', 'plomería', 'electricidad', 'gas'],
            'acabados': ['acabados', 'pintura', 'pisos', 'revestimientos']
        }
    
    def configurar_fecha_inicio(self, fecha_inicio):
        """
        Configura la fecha de inicio del proyecto.
        
        Args:
            fecha_inicio (str o datetime): Fecha de inicio en formato 'YYYY-MM-DD' o datetime
        """
        if isinstance(fecha_inicio, str):
            try:
                self.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except ValueError:
                try:
                    self.fecha_inicio = datetime.strptime(fecha_inicio, '%d/%m/%Y').date()
                except ValueError:
                    print("Error: Formato de fecha no válido. Use 'YYYY-MM-DD' o 'DD/MM/YYYY'")
                    return False
        elif isinstance(fecha_inicio, datetime):
            self.fecha_inicio = fecha_inicio.date()
        else:
            print("Error: Tipo de fecha no válido")
            return False
        
        print(f"Fecha de inicio configurada: {self.fecha_inicio}")
        
        # Si ya hay un cronograma, recalcularlo con la nueva fecha
        if self.df_actividades is not None:
            print("Recalculando cronograma con nueva fecha de inicio...")
            # Crear una copia del DataFrame sin las columnas de fecha
            df_sin_fechas = self.df_actividades[['Actividad', 'Duración', 'Predecesoras']].copy()
            self.df_actividades = self.generar_cronograma(df_sin_fechas)
            print("Cronograma recalculado exitosamente")
        
        return True
        
        # Duración estimada por tipo de actividad (en días)
        self.duraciones_estimadas = {
            'excavacion': 5,
            'cimentacion': 10,
            'estructura': 15,
            'muros': 8,
            'techos': 6,
            'instalaciones': 12,
            'acabados': 10
        }
    
    def leer_entrada(self, entrada: str) -> pd.DataFrame:
        """
        Procesa la entrada del usuario (texto natural o ruta de archivo CSV).
        
        Args:
            entrada (str): Texto descriptivo del proyecto o ruta a archivo CSV
            
        Returns:
            pd.DataFrame: DataFrame con columnas [Actividad, Duración, Predecesoras]
        """
        print(f"Procesando entrada: {entrada[:50]}...")
        
        # Verificar si es una ruta de archivo
        if entrada.lower().endswith(('.csv', '.xlsx', '.xls')):
            return self._leer_archivo(entrada)
        else:
            return self._procesar_texto_natural(entrada)
    
    def _leer_archivo(self, ruta_archivo: str) -> pd.DataFrame:
        """
        Lee y procesa un archivo CSV o Excel.
        
        Args:
            ruta_archivo (str): Ruta al archivo
            
        Returns:
            pd.DataFrame: DataFrame procesado
        """
        try:
            if ruta_archivo.endswith('.csv'):
                # Leer el CSV con configuración específica para este formato
                df = pd.read_csv(ruta_archivo, encoding='utf-8', sep=',', quotechar='"', skipinitialspace=True, doublequote=True)
            else:
                df = pd.read_excel(ruta_archivo)
            
            # Normalizar nombres de columnas
            df.columns = df.columns.str.strip().str.lower()
            
            # Verificar si es el formato con Nombre, Duracion, Comienzo, Fin
            if 'nombre' in df.columns and 'duracion' in df.columns and 'comienzo' in df.columns:
                print("Detectado formato con columnas Nombre, Duracion, Comienzo, Fin...")
                return self._procesar_formato_nombre_duracion(df)
            
            # Mapear nombres de columnas comunes
            mapeo_columnas = {
                'actividad': 'Actividad',
                'tarea': 'Actividad',
                'task': 'Actividad',
                'nombre': 'Actividad',
                'duracion': 'Duración',
                'duration': 'Duración',
                'dias': 'Duración',
                'predecesoras': 'Predecesoras',
                'predecessors': 'Predecesoras',
                'dependencias': 'Predecesoras'
            }
            
            df = df.rename(columns=mapeo_columnas)
            
            # Validar que existan las columnas necesarias
            columnas_requeridas = ['Actividad', 'Duración']
            for col in columnas_requeridas:
                if col not in df.columns:
                    raise ValueError(f"Columna '{col}' no encontrada en el archivo")
            
            # Agregar columna Predecesoras si no existe
            if 'Predecesoras' not in df.columns:
                df['Predecesoras'] = ''
            
            # Limpiar datos
            df['Predecesoras'] = df['Predecesoras'].fillna('').astype(str)
            df['Duración'] = pd.to_numeric(df['Duración'], errors='coerce')
            
            # Filtrar filas con duración válida
            df = df[df['Duración'] > 0]
            
            print(f"Archivo leído exitosamente: {len(df)} actividades encontradas")
            return df[['Actividad', 'Duración', 'Predecesoras']]
            
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            return self._crear_dataframe_ejemplo()
    
    def _procesar_formato_nombre_duracion(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Procesa el formato con columnas Nombre, Duracion, Comienzo, Fin.
        Este CSV tiene un formato especial donde los datos están en comillas anidadas.
        
        Args:
            df (pd.DataFrame): DataFrame con el formato nombre/duracion
            
        Returns:
            pd.DataFrame: DataFrame procesado en formato estándar
        """
        try:
            actividades_procesadas = []
            fecha_inicio_proyecto = None
            
            # Verificar si los datos están en la primera columna (formato con comillas anidadas)
            primera_columna = df.columns[0].lower()
            
            if 'nombre' in primera_columna:
                # Los datos están mezclados en la primera columna
                # Necesitamos parsear cada fila manualmente
                for _, row in df.iterrows():
                    fila_str = str(row[df.columns[0]])
                    
                    if pd.isna(fila_str) or fila_str == 'nan':
                        continue
                    
                    # Parsear la fila para extraer campos
                    campos = self._parsear_fila_csv_especial(fila_str)
                    
                    if campos and len(campos) >= 7:
                        nombre = campos[0]
                        duracion_str = campos[4]
                        comienzo_str = campos[5]
                        fin_str = campos[6]
                        
                        # Extraer duración numérica
                        if 'día' in duracion_str.lower():
                            match = re.search(r'(\d+(?:[.,]\d+)?)\s*d[ií]as?', duracion_str, re.IGNORECASE)
                            if match:
                                duracion_num = float(match.group(1).replace(',', '.'))
                                duracion_int = round(duracion_num)
                                
                                if duracion_int > 0:
                                    # Parsear fecha de inicio
                                    fecha_inicio = self._parsear_fecha_espanol(comienzo_str)
                                    fecha_fin = self._parsear_fecha_espanol(fin_str)
                                    
                                    # Guardar la primera fecha de inicio válida
                                    if fecha_inicio and not fecha_inicio_proyecto:
                                        fecha_inicio_proyecto = fecha_inicio
                                    
                                    actividades_procesadas.append({
                                        'Actividad': nombre,
                                        'Duración': duracion_int,
                                        'Predecesoras': ''
                                    })
            else:
                # Formato normal con columnas separadas
                for _, row in df.iterrows():
                    nombre = str(row['nombre']).strip()
                    
                    if pd.isna(nombre) or nombre == '' or nombre == 'nan':
                        continue
                    
                    duracion_str = str(row['duracion']).strip()
                    
                    if 'día' in duracion_str.lower():
                        match = re.search(r'(\d+(?:[.,]\d+)?)\s*d[ií]as?', duracion_str, re.IGNORECASE)
                        if match:
                            duracion_num = float(match.group(1).replace(',', '.'))
                            duracion_int = round(duracion_num)
                            
                            if duracion_int > 0:
                                # Intentar parsear fecha de inicio si existe
                                if 'comienzo' in df.columns:
                                    comienzo_str = str(row['comienzo'])
                                    fecha_inicio = self._parsear_fecha_espanol(comienzo_str)
                                    if fecha_inicio and not fecha_inicio_proyecto:
                                        fecha_inicio_proyecto = fecha_inicio
                                
                                actividades_procesadas.append({
                                    'Actividad': nombre,
                                    'Duración': duracion_int,
                                    'Predecesoras': ''
                                })
            
            if not actividades_procesadas:
                raise ValueError("No se encontraron actividades válidas en el archivo")
            
            # Si encontramos una fecha de inicio en el archivo, usarla
            if fecha_inicio_proyecto:
                self.fecha_inicio = fecha_inicio_proyecto.date()
                print(f"Fecha de inicio detectada del archivo: {self.fecha_inicio}")
            
            df_resultado = pd.DataFrame(actividades_procesadas)
            print(f"Archivo procesado: {len(df_resultado)} actividades encontradas")
            return df_resultado
            
        except Exception as e:
            print(f"Error al procesar archivo: {e}")
            import traceback
            traceback.print_exc()
            return self._crear_dataframe_ejemplo()
    
    def _parsear_fila_csv_especial(self, fila_str: str) -> list:
        """
        Parsea una fila del CSV que tiene campos separados por comas con comillas anidadas.
        Formato: "campo1","campo2",campo3,campo4,"campo5",...
        
        Args:
            fila_str (str): String de la fila a parsear
            
        Returns:
            list: Lista de campos extraídos
        """
        campos = []
        actual = ""
        dentro_comillas = False
        
        i = 0
        while i < len(fila_str):
            char = fila_str[i]
            
            if char == '"':
                # Verificar si es comilla doble escapada
                if i + 1 < len(fila_str) and fila_str[i + 1] == '"':
                    actual += '"'
                    i += 2
                    continue
                else:
                    dentro_comillas = not dentro_comillas
                    i += 1
                    continue
            
            if char == ',' and not dentro_comillas:
                # Fin de campo
                campos.append(actual.strip())
                actual = ""
                i += 1
                continue
            
            actual += char
            i += 1
        
        # Agregar último campo
        if actual:
            campos.append(actual.strip())
        
        return campos
    
    def _parsear_fecha_espanol(self, fecha_str: str):
        """
        Parsea una fecha en formato español.
        Soporta formatos: "DD mes YYYY H:MM a./p. m." y variantes
        
        Args:
            fecha_str (str): String con la fecha a parsear
            
        Returns:
            datetime o None: Fecha parseada o None si falla
        """
        if not fecha_str or fecha_str == 'nan':
            return None
            
        try:
            from datetime import datetime
            
            # Patrón para fechas en español: "DD mes YYYY H:MM a./p. m."
            patron = r'(\d{1,2})\s+(\w+)\s+(\d{4})\s+(\d{1,2}):(\d{2})\s+(a\.|p\.)\s+m\.'
            match = re.search(patron, fecha_str)
            
            if match:
                dia, mes_str, año, hora, minuto, periodo = match.groups()
                
                # Mapeo de meses en español
                meses = {
                    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
                    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
                    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
                }
                
                mes = meses.get(mes_str.lower())
                if mes:
                    hora_int = int(hora)
                    if periodo == 'p.' and hora_int != 12:
                        hora_int += 12
                    elif periodo == 'a.' and hora_int == 12:
                        hora_int = 0
                    
                    return datetime(int(año), mes, int(dia), hora_int, int(minuto))
            
            return None
        except Exception as e:
            print(f"Error al parsear fecha '{fecha_str}': {e}")
            return None
    
    def _procesar_texto_natural(self, texto: str) -> pd.DataFrame:
        """
        Extrae actividades, duraciones y dependencias de texto en lenguaje natural.
        Usa Gemini AI si está disponible, sino usa regex como fallback.
        
        Args:
            texto (str): Descripción del proyecto en lenguaje natural
            
        Returns:
            pd.DataFrame: DataFrame con las actividades extraídas
        """
        print("Analizando descripción del proyecto...")
        
        # Intentar usar Gemini AI primero
        if GEMINI_AVAILABLE:
            try:
                gemini_service = get_gemini_service()
                if gemini_service:
                    print("Usando Gemini AI para análisis...")
                    resultado_gemini = gemini_service.analizar_proyecto_construccion(texto)
                    
                    if resultado_gemini and resultado_gemini.get('actividades'):
                        actividades_extraidas = resultado_gemini['actividades']
                        print(f"Gemini AI analizó el proyecto: {len(actividades_extraidas)} actividades identificadas")
                        
                        # Mostrar análisis de Gemini si está disponible
                        if resultado_gemini.get('analisis'):
                            print(f"Análisis de IA: {resultado_gemini['analisis']}")
                        
                        df = pd.DataFrame(actividades_extraidas)
                        return df
                    else:
                        print("Gemini no pudo analizar el proyecto, usando fallback...")
                else:
                    print("Gemini no configurado, usando fallback...")
            except Exception as e:
                print(f"Error con Gemini: {e}, usando fallback...")
        
        # Fallback: usar regex como antes
        print("Usando análisis con regex...")
        actividades_extraidas = []
        
        # Dividir el texto en líneas para procesar cada actividad
        lineas = texto.split('\n')
        
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            
            # Intentar extraer actividad, duración y dependencias con regex
            actividad_extraida = self._extraer_actividad_con_regex(linea)
            if actividad_extraida:
                actividades_extraidas.append(actividad_extraida)
        
        # Si no se encontraron actividades con regex, usar el método anterior
        if not actividades_extraidas:
            print("No se detectaron actividades específicas, usando detección por patrones...")
            actividades_extraidas = self._procesar_por_patrones(texto)
        
        # Si aún no hay actividades, crear proyecto básico
        if not actividades_extraidas:
            print("Creando proyecto básico...")
            actividades_extraidas = self._crear_proyecto_basico(texto)
        
        df = pd.DataFrame(actividades_extraidas)
        print(f"Proyecto analizado: {len(df)} actividades identificadas")
        
        return df
    
    def _extraer_actividad_con_regex(self, linea: str) -> Optional[Dict]:
        """
        Extrae actividad, duración y dependencias de una línea usando regex.
        
        Args:
            linea (str): Línea de texto a procesar
            
        Returns:
            Optional[Dict]: Diccionario con la actividad extraída o None
        """
        # Patrones regex para diferentes formatos
        patrones = [
            # Formato: "Actividad — X días (después de Predecesora)"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*[-–—]\s*(?P<duracion>\d+)\s*d[ií]as?\s*\(despu[eé]s de\s+(?P<predecesora>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+)\)',
            
            # Formato: "Actividad - X días después de Predecesora"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*[-–—]\s*(?P<duracion>\d+)\s*d[ií]as?\s+despu[eé]s de\s+(?P<predecesora>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+)',
            
            # Formato: "Actividad: X días después de Predecesora"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*:\s*(?P<duracion>\d+)\s*d[ií]as?\s+despu[eé]s de\s+(?P<predecesora>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+)',
            
            # Formato: "Actividad: X días (Predecesora)"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*:\s*(?P<duracion>\d+)\s*d[ií]as?\s*\((?P<predecesora>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+)\)',
            
            # Formato: "Actividad — X días (Predecesora)"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*[-–—]\s*(?P<duracion>\d+)\s*d[ií]as?\s*\((?P<predecesora>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+)\)',
            
            # Formato: "Actividad — X días: Predecesora"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*[-–—]\s*(?P<duracion>\d+)\s*d[ií]as?\s*:\s*(?P<predecesora>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+)',
            
            # Formato: "Actividad: X días Predecesora" (sin paréntesis)
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*:\s*(?P<duracion>\d+)\s*d[ií]as?\s+(?P<predecesora>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)(?:\s|$)',
            
            # Formato: "Actividad - X días"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*[-–—]\s*(?P<duracion>\d+)\s*d[ií]as?',
            
            # Formato: "Actividad: X días"
            r'(\d+\.\s*)?(?P<actividad>[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s*:\s*(?P<duracion>\d+)\s*d[ií]as?',
        ]
        
        for patron in patrones:
            match = re.search(patron, linea, re.IGNORECASE)
            if match:
                actividad = match.group('actividad').strip()
                duracion = int(match.group('duracion'))
                
                # Extraer predecesora si existe
                predecesora = match.group('predecesora').strip() if 'predecesora' in match.groupdict() and match.group('predecesora') else ''
                
                return {
                    'Actividad': actividad,
                    'Duración': duracion,
                    'Predecesoras': predecesora
                }
        
        return None
    
    def _procesar_por_patrones(self, texto: str) -> List[Dict]:
        """
        Procesa el texto usando el método anterior de detección por patrones.
        
        Args:
            texto (str): Texto del proyecto
            
        Returns:
            List[Dict]: Lista de actividades extraídas
        """
        actividades_extraidas = []
        texto_lower = texto.lower()
        
        # Buscar patrones de actividades
        for tipo_actividad, patrones in self.patrones_actividades.items():
            for patron in patrones:
                if patron in texto_lower:
                    duracion = self.duraciones_estimadas[tipo_actividad]
                    actividades_extraidas.append({
                        'Actividad': tipo_actividad.title(),
                        'Duración': duracion,
                        'Predecesoras': ''
                    })
                    break
        
        # Establecer dependencias lógicas si se encontraron actividades
        if actividades_extraidas:
            actividades_extraidas = self._establecer_dependencias(actividades_extraidas)
        
        return actividades_extraidas
    
    def _crear_proyecto_basico(self, texto: str) -> List[Dict]:
        """
        Crea un proyecto básico cuando no se detectan actividades específicas.
        
        Args:
            texto (str): Texto del proyecto
            
        Returns:
            List[Dict]: Lista de actividades básicas
        """
        # Proyecto básico de construcción
        actividades_basicas = [
            {'Actividad': 'Excavación', 'Duración': 5, 'Predecesoras': ''},
            {'Actividad': 'Cimentación', 'Duración': 10, 'Predecesoras': 'Excavación'},
            {'Actividad': 'Estructura', 'Duración': 15, 'Predecesoras': 'Cimentación'},
            {'Actividad': 'Muros', 'Duración': 8, 'Predecesoras': 'Estructura'},
            {'Actividad': 'Techos', 'Duración': 6, 'Predecesoras': 'Muros'},
            {'Actividad': 'Instalaciones', 'Duración': 12, 'Predecesoras': 'Techos'},
            {'Actividad': 'Acabados', 'Duración': 10, 'Predecesoras': 'Instalaciones'}
        ]
        
        return actividades_basicas
    
    def _establecer_dependencias(self, actividades: List[Dict]) -> List[Dict]:
        """
        Establece dependencias lógicas entre actividades.
        
        Args:
            actividades (List[Dict]): Lista de actividades
            
        Returns:
            List[Dict]: Lista de actividades con dependencias establecidas
        """
        # Orden lógico de construcción
        orden_logico = ['Excavación', 'Cimentación', 'Estructura', 'Muros', 'Techos', 'Instalaciones', 'Acabados']
        
        for i, actividad in enumerate(actividades):
            nombre_actividad = actividad['Actividad']
            
            # Buscar la posición en el orden lógico
            try:
                posicion = orden_logico.index(nombre_actividad)
                if posicion > 0:
                    actividad['Predecesoras'] = orden_logico[posicion - 1]
            except ValueError:
                # Si no está en el orden lógico, mantener dependencias existentes
                pass
        
        return actividades
    
    def _crear_dataframe_ejemplo(self) -> pd.DataFrame:
        """
        Crea un DataFrame de ejemplo cuando hay errores en la entrada.
        
        Returns:
            pd.DataFrame: DataFrame con proyecto de ejemplo
        """
        print("Creando proyecto de ejemplo...")
        
        actividades_ejemplo = [
            {'Actividad': 'Excavación', 'Duración': 5, 'Predecesoras': ''},
            {'Actividad': 'Cimentación', 'Duración': 10, 'Predecesoras': 'Excavación'},
            {'Actividad': 'Estructura', 'Duración': 15, 'Predecesoras': 'Cimentación'},
            {'Actividad': 'Muros', 'Duración': 8, 'Predecesoras': 'Estructura'},
            {'Actividad': 'Techos', 'Duración': 6, 'Predecesoras': 'Muros'},
            {'Actividad': 'Instalaciones', 'Duración': 12, 'Predecesoras': 'Techos'},
            {'Actividad': 'Acabados', 'Duración': 10, 'Predecesoras': 'Instalaciones'}
        ]
        
        return pd.DataFrame(actividades_ejemplo)
    
    def generar_cronograma(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula las fechas de inicio y fin para cada actividad basándose en las dependencias.
        Versión corregida que respeta las dependencias secuenciales.
        
        Args:
            df (pd.DataFrame): DataFrame con actividades y dependencias
            
        Returns:
            pd.DataFrame: DataFrame con fechas calculadas
        """
        print("Generando cronograma...")
        
        df_cronograma = df.copy()
        
        # Diccionarios para almacenar fechas de inicio y fin
        inicio = {}
        fin = {}
        
        # Procesar cada actividad respetando dependencias
        for i, row in df_cronograma.iterrows():
            actividad = row["Actividad"]
            duracion = int(row["Duración"])
            predecesoras = str(row["Predecesoras"]).strip()
            
            # Si no tiene predecesoras, inicia en el día 0 (fecha de inicio del proyecto)
            if not predecesoras or predecesoras == '' or predecesoras.lower() == 'nan':
                inicio[actividad] = self.fecha_inicio
            else:
                # Si tiene predecesoras, inicia después de que termine la última
                predecesoras_lista = [p.strip() for p in predecesoras.split(',')]
                max_fin = self.fecha_inicio  # Inicializar con fecha de inicio
                
                for pred in predecesoras_lista:
                    if pred and pred in fin:
                        if fin[pred] > max_fin:
                            max_fin = fin[pred]
                
                inicio[actividad] = max_fin
            
            # Calcular fecha de fin
            fin[actividad] = inicio[actividad] + timedelta(days=duracion)
        
        # Asignar fechas al DataFrame
        df_cronograma['Fecha_Inicio'] = df_cronograma['Actividad'].map(inicio)
        df_cronograma['Fecha_Fin'] = df_cronograma['Actividad'].map(fin)
        
        # Calcular duración total del proyecto
        fecha_fin_proyecto = df_cronograma['Fecha_Fin'].max()
        duracion_total = (fecha_fin_proyecto - self.fecha_inicio).days
        
        print(f"Cronograma generado: {duracion_total} días de duración total")
        print(f"Actividades procesadas: {len(df_cronograma)}")
        
        return df_cronograma
    
    def mostrar_gantt(self, df: pd.DataFrame) -> None:
        """
        Genera y muestra un diagrama de Gantt interactivo usando Plotly.
        
        Args:
            df (pd.DataFrame): DataFrame con el cronograma
        """
        print("Generando diagrama de Gantt...")
        
        # Preparar datos para Plotly
        fig = go.Figure()
        
        # Colores para diferentes tipos de actividades
        colores = px.colors.qualitative.Set3
        
        for i, row in df.iterrows():
            color = colores[i % len(colores)]
            
            fig.add_trace(go.Scatter(
                x=[row['Fecha_Inicio'], row['Fecha_Fin']],
                y=[row['Actividad'], row['Actividad']],
                mode='lines+markers',
                line=dict(color=color, width=8),
                marker=dict(size=8),
                name=row['Actividad'],
                hovertemplate=f"<b>{row['Actividad']}</b><br>" +
                             f"Inicio: {row['Fecha_Inicio'].strftime('%d/%m/%Y')}<br>" +
                             f"Fin: {row['Fecha_Fin'].strftime('%d/%m/%Y')}<br>" +
                             f"Duración: {row['Duración']} días<br>" +
                             f"Predecesoras: {row['Predecesoras']}<extra></extra>"
            ))
        
        # Configurar el layout
        fig.update_layout(
            title={
                'text': '📅 Cronograma de Construcción - Diagrama de Gantt',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis_title='Fecha',
            yaxis_title='Actividades',
            height=400 + len(df) * 40,
            showlegend=False,
            hovermode='closest',
            xaxis=dict(
                tickformat='%d/%m/%Y',
                tickangle=45
            ),
            yaxis=dict(
                categoryorder='category ascending'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Mostrar el gráfico
        fig.show()
        
        # Mostrar resumen del cronograma
        self._mostrar_resumen_cronograma(df)
    
    def _mostrar_resumen_cronograma(self, df: pd.DataFrame) -> None:
        """
        Muestra un resumen del cronograma generado.
        
        Args:
            df (pd.DataFrame): DataFrame con el cronograma
        """
        print("\n" + "="*60)
        print("RESUMEN DEL CRONOGRAMA")
        print("="*60)
        
        duracion_total = (df['Fecha_Fin'].max() - df['Fecha_Inicio'].min()).days
        
        print(f"Fecha de inicio: {df['Fecha_Inicio'].min().strftime('%d/%m/%Y')}")
        print(f"Fecha de fin: {df['Fecha_Fin'].max().strftime('%d/%m/%Y')}")
        print(f"Duración total: {duracion_total} días")
        print(f"Total de actividades: {len(df)}")
        
        print("\nDETALLE DE ACTIVIDADES:")
        print("-" * 60)
        for _, row in df.iterrows():
            # Formatear predecesoras con flecha visual
            predecesoras = row['Predecesoras']
            if predecesoras and predecesoras != '':
                predecesoras_texto = f"{predecesoras} → {row['Actividad']}"
            else:
                predecesoras_texto = f"[Inicio] → {row['Actividad']}"
            
            print(f"• {row['Actividad']:<20} | "
                  f"{row['Fecha_Inicio'].strftime('%d/%m')} - "
                  f"{row['Fecha_Fin'].strftime('%d/%m')} | "
                  f"{row['Duración']:>2} días | "
                  f"{predecesoras_texto}")
        
        print("="*60)
    
    def optimizar_cronograma(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimiza el cronograma reduciendo duraciones y permitiendo tareas paralelas.
        
        Args:
            df (pd.DataFrame): DataFrame con el cronograma original
            
        Returns:
            pd.DataFrame: DataFrame con el cronograma optimizado
        """
        print("🚀 Optimizando cronograma...")
        
        df_optimizado = df.copy()
        
        # Reducir duraciones de tareas largas (más de 10 días)
        tareas_largas = df_optimizado[df_optimizado['Duración'] > 10]
        if len(tareas_largas) > 0:
            print(f"Reduciendo duración de {len(tareas_largas)} tareas largas...")
            df_optimizado.loc[df_optimizado['Duración'] > 10, 'Duración'] = \
                df_optimizado.loc[df_optimizado['Duración'] > 10, 'Duración'] * 0.8
        
        # Identificar tareas que pueden ejecutarse en paralelo
        tareas_paralelas = self._identificar_tareas_paralelas(df_optimizado)
        if tareas_paralelas:
            print(f"Identificando {len(tareas_paralelas)} oportunidades de paralelización...")
            df_optimizado = self._aplicar_paralelizacion(df_optimizado, tareas_paralelas)
        
        # Recalcular el cronograma con las optimizaciones
        df_optimizado = self.generar_cronograma(df_optimizado)
        
        # Mostrar mejoras
        duracion_original = (df['Fecha_Fin'].max() - df['Fecha_Inicio'].min()).days
        duracion_optimizada = (df_optimizado['Fecha_Fin'].max() - df_optimizado['Fecha_Inicio'].min()).days
        mejora = duracion_original - duracion_optimizada
        porcentaje_mejora = (mejora / duracion_original) * 100
        
        print(f"Optimización completada!")
        print(f"Reducción de tiempo: {mejora} días ({porcentaje_mejora:.1f}%)")
        print(f"Nueva duración: {duracion_optimizada} días")
        
        return df_optimizado
    
    def _identificar_tareas_paralelas(self, df: pd.DataFrame) -> List[Tuple[str, str]]:
        """
        Identifica tareas que pueden ejecutarse en paralelo.
        
        Args:
            df (pd.DataFrame): DataFrame con actividades
            
        Returns:
            List[Tuple[str, str]]: Lista de pares de tareas que pueden paralelizarse
        """
        tareas_paralelas = []
        
        # Tareas que típicamente pueden ejecutarse en paralelo
        pares_paralelos = [
            ('Muros', 'Instalaciones'),
            ('Techos', 'Acabados'),
            ('Instalaciones', 'Acabados')
        ]
        
        actividades_disponibles = df['Actividad'].tolist()
        
        for tarea1, tarea2 in pares_paralelos:
            if tarea1 in actividades_disponibles and tarea2 in actividades_disponibles:
                tareas_paralelas.append((tarea1, tarea2))
        
        return tareas_paralelas
    
    def _aplicar_paralelizacion(self, df: pd.DataFrame, tareas_paralelas: List[Tuple[str, str]]) -> pd.DataFrame:
        """
        Aplica paralelización a las tareas identificadas.
        
        Args:
            df (pd.DataFrame): DataFrame con actividades
            tareas_paralelas (List[Tuple[str, str]]): Lista de tareas a paralelizar
            
        Returns:
            pd.DataFrame: DataFrame con paralelización aplicada
        """
        df_paralelo = df.copy()
        
        for tarea1, tarea2 in tareas_paralelas:
            # Encontrar índices de las tareas
            idx1 = df_paralelo[df_paralelo['Actividad'] == tarea1].index[0]
            idx2 = df_paralelo[df_paralelo['Actividad'] == tarea2].index[0]
            
            # Modificar dependencias para permitir paralelización
            # La segunda tarea puede empezar cuando termine la predecesora común
            predecesora_comun = df_paralelo.loc[idx1, 'Predecesoras']
            if predecesora_comun:
                df_paralelo.loc[idx2, 'Predecesoras'] = predecesora_comun
        
        return df_paralelo
    
    def responder_pregunta(self, pregunta: str, df: pd.DataFrame) -> str:
        """
        Interpreta y responde preguntas sobre el cronograma en lenguaje natural.
        
        Args:
            pregunta (str): Pregunta del usuario
            df (pd.DataFrame): DataFrame con el cronograma
            
        Returns:
            str: Respuesta generada
        """
        # Intentar usar Gemini AI primero
        if GEMINI_AVAILABLE:
            try:
                gemini_service = get_gemini_service()
                if gemini_service:
                    # Preparar contexto para Gemini
                    contexto = {
                        "actividades": df.to_dict('records'),
                        "duracion_total": (df['Fecha_Fin'].max() - df['Fecha_Inicio'].min()).days,
                        "fecha_inicio": df['Fecha_Inicio'].min().strftime('%d/%m/%Y'),
                        "fecha_fin": df['Fecha_Fin'].max().strftime('%d/%m/%Y'),
                        "total_actividades": len(df)
                    }
                    
                    # Convertir fechas a strings para evitar problemas de serialización
                    for actividad in contexto["actividades"]:
                        if 'Fecha_Inicio' in actividad:
                            actividad['Fecha_Inicio'] = actividad['Fecha_Inicio'].strftime('%d/%m/%Y')
                        if 'Fecha_Fin' in actividad:
                            actividad['Fecha_Fin'] = actividad['Fecha_Fin'].strftime('%d/%m/%Y')
                    
                    respuesta_gemini = gemini_service.responder_pregunta_cronograma(pregunta, contexto)
                    if respuesta_gemini and len(respuesta_gemini.strip()) > 10:
                        return respuesta_gemini
            except Exception as e:
                print(f"Error con Gemini en responder_pregunta: {e}")
        
        # Fallback: usar lógica predefinida
        pregunta_lower = pregunta.lower()
        
        # Análisis de la duración del proyecto
        if any(palabra in pregunta_lower for palabra in ['duración', 'tiempo', 'cuánto', 'días']):
            duracion_total = (df['Fecha_Fin'].max() - df['Fecha_Inicio'].min()).days
            return f"El proyecto tiene una duración total de {duracion_total} días, desde el {df['Fecha_Inicio'].min().strftime('%d/%m/%Y')} hasta el {df['Fecha_Fin'].max().strftime('%d/%m/%Y')}."
        
        # Análisis de tareas paralelas
        elif any(palabra in pregunta_lower for palabra in ['paralelo', 'simultáneo', 'mismo tiempo']):
            tareas_paralelas = self._identificar_tareas_paralelas(df)
            if tareas_paralelas:
                respuesta = "Las siguientes tareas pueden ejecutarse en paralelo:\n"
                for tarea1, tarea2 in tareas_paralelas:
                    respuesta += f"• {tarea1} y {tarea2}\n"
                return respuesta
            else:
                return "En el cronograma actual, todas las tareas están secuencialmente dependientes. Se podrían optimizar algunas para ejecutarse en paralelo."
        
        # Optimización del cronograma
        elif any(palabra in pregunta_lower for palabra in ['optimizar', 'mejorar', 'reducir', 'acelerar']):
            return "Para optimizar el cronograma, puedo:\n• Reducir la duración de tareas largas\n• Identificar oportunidades de paralelización\n• Recalcular las fechas\n\n¿Te gustaría que aplique estas optimizaciones?"
        
        # Análisis de la ruta crítica
        elif any(palabra in pregunta_lower for palabra in ['crítica', 'crítico', 'ruta']):
            return "La ruta crítica es la secuencia de tareas que determina la duración mínima del proyecto. En tu cronograma, todas las tareas están en la ruta crítica debido a las dependencias secuenciales."
        
        # Información sobre actividades específicas
        elif any(palabra in pregunta_lower for palabra in ['actividad', 'tarea', 'qué']):
            respuesta = "Las actividades del proyecto son:\n"
            for _, row in df.iterrows():
                respuesta += f"• {row['Actividad']}: {row['Duración']} días\n"
            return respuesta
        
        # Pregunta no reconocida
        else:
            return "No estoy seguro de cómo responder esa pregunta. Puedo ayudarte con:\n• Duración del proyecto\n• Tareas paralelas\n• Optimización del cronograma\n• Información sobre actividades específicas\n\n¿Podrías reformular tu pregunta?"
    
    def iniciar_chat(self) -> None:
        """
        Inicia la interfaz de chat interactiva.
        """
        print("\n" + "="*80)
        print("AI BUILDER SCHEDULER - Asistente Inteligente de Cronogramas")
        print("="*80)
        print("¡Hola! Soy tu asistente de IA para cronogramas de construcción.")
        print("Puedo ayudarte a generar, analizar y optimizar cronogramas de proyectos.")
        print("\nOpciones de entrada:")
        print("• Describe tu proyecto en lenguaje natural")
        print("• Proporciona la ruta a un archivo CSV con actividades")
        print("• Escribe 'ejemplo' para usar un proyecto de demostración")
        print("\nComandos especiales:")
        print("• 'optimizar' - Optimiza el cronograma actual")
        print("• 'mostrar' - Muestra el diagrama de Gantt")
        print("• 'salir' - Termina la sesión")
        print("="*80)
        
        # Obtener entrada inicial
        entrada = input("\n💬 ¿Cómo puedo ayudarte? ").strip()
        
        if entrada.lower() == 'salir':
            print("👋 ¡Hasta luego!")
            return
        
        # Procesar entrada inicial
        if entrada.lower() == 'ejemplo':
            entrada = "Construir una casa de dos pisos con excavación, cimentación, estructura y acabados."
        
        self.df_actividades = self.leer_entrada(entrada)
        self.df_actividades = self.generar_cronograma(self.df_actividades)
        self.mostrar_gantt(self.df_actividades)
        
        # Loop de conversación
        while self.conversacion_activa:
            pregunta = input("\n💬 ¿Tienes alguna pregunta sobre el cronograma? ").strip()
            
            if pregunta.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Gracias por usar AI Builder Scheduler!")
                self.conversacion_activa = False
                break
            
            elif pregunta.lower() == 'optimizar':
                print("\n🚀 Aplicando optimizaciones...")
                self.df_actividades = self.optimizar_cronograma(self.df_actividades)
                self.mostrar_gantt(self.df_actividades)
            
            elif pregunta.lower() == 'mostrar':
                self.mostrar_gantt(self.df_actividades)
            
            else:
                respuesta = self.responder_pregunta(pregunta, self.df_actividades)
                print(f"\n🤖 {respuesta}")


def main():
    """
    Función principal que ejecuta el AI Builder Scheduler.
    """
    try:
        scheduler = AIBuilderScheduler()
        scheduler.iniciar_chat()
    except KeyboardInterrupt:
        print("\n\n👋 Sesión interrumpida por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("Por favor, verifica tu entrada e intenta nuevamente.")


if __name__ == "__main__":
    main()


# =============================================================================
# EJEMPLO DE CONVERSACIÓN
# =============================================================================

"""
EJEMPLO DE USO DEL AI BUILDER SCHEDULER
=======================================

Usuario: "Construir una casa de dos pisos con excavación, cimentación, estructura y acabados."

AI: 🔍 Procesando entrada: Construir una casa de dos pisos con excavación...
🧠 Analizando descripción del proyecto...
✅ Proyecto analizado: 4 actividades identificadas
📅 Generando cronograma...
✅ Cronograma generado: 40 días de duración total
📊 Generando diagrama de Gantt...

[Se muestra el diagrama de Gantt interactivo]

📋 RESUMEN DEL CRONOGRAMA
============================================================
📅 Fecha de inicio: 15/01/2025
📅 Fecha de fin: 25/02/2025
⏱️  Duración total: 40 días
📊 Total de actividades: 4

📝 DETALLE DE ACTIVIDADES:
------------------------------------------------------------
• Excavación           | 15/01 - 20/01 |  5 días | Predecesoras: 
• Cimentación          | 20/01 - 30/01 | 10 días | Predecesoras: Excavación
• Estructura           | 30/01 - 14/02 | 15 días | Predecesoras: Cimentación
• Acabados             | 14/02 - 25/02 | 10 días | Predecesoras: Estructura
============================================================

Usuario: "¿Cuánto dura el proyecto?"

AI: 🤖 📅 El proyecto tiene una duración total de 40 días, desde el 15/01/2025 hasta el 25/02/2025.

Usuario: "optimizar"

AI: 🚀 Aplicando optimizaciones...
🚀 Optimizando cronograma...
⚡ Reduciendo duración de 1 tareas largas...
🔄 Identificando 0 oportunidades de paralelización...
✅ Optimización completada!
📉 Reducción de tiempo: 3 días (7.5%)
⏱️  Nueva duración: 37 días

[Se muestra el nuevo diagrama de Gantt optimizado]

Usuario: "¿Qué tareas puedo hacer en paralelo?"

AI: 🤖 🔄 Las siguientes tareas pueden ejecutarse en paralelo:
• Muros y Instalaciones
• Techos y Acabados

Usuario: "salir"

AI: 👋 ¡Gracias por usar AI Builder Scheduler!
"""
