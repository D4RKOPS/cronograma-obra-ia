#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend Flask para AI Builder Scheduler
=======================================

API REST que proporciona endpoints para la aplicación web React.
Maneja la lógica del AI Builder Scheduler y sirve datos JSON.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
import json
import os
import sys
from datetime import datetime, timedelta
import re
from typing import Dict, List, Tuple, Optional, Union

# Agregar el directorio padre al path para importar el scheduler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_builder_scheduler import AIBuilderScheduler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://cronograma-obra-ia.vercel.app"}})

# Instancia global del scheduler
scheduler = AIBuilderScheduler()

@app.route('/')
def index():
    """Endpoint raíz - redirige a la documentación de la API."""
    return jsonify({
        "message": "AI Builder Scheduler API",
        "version": "1.0",
        "endpoints": {
            "POST /api/process": "Procesar entrada (texto o archivo)",
            "POST /api/optimize": "Optimizar cronograma",
            "GET /api/chat": "Chat con el asistente",
            "GET /api/status": "Estado del sistema"
        }
    })

@app.route('/api/process', methods=['POST'])
def process_input():
    """
    Procesa entrada del usuario (texto natural o archivo CSV).
    
    Body JSON:
    {
        "input": "texto del proyecto" o "ruta del archivo",
        "type": "text" o "file"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({"error": "Input requerido"}), 400
        
        input_text = data['input']
        input_type = data.get('type', 'text')
        
        # Procesar entrada
        df_actividades = scheduler.leer_entrada(input_text)
        df_cronograma = scheduler.generar_cronograma(df_actividades)
        
        # Generar gráfico de Gantt
        gantt_data = generate_gantt_data(df_cronograma)
        
        # Preparar respuesta
        response = {
            "success": True,
            "activities": df_cronograma.to_dict('records'),
            "gantt_data": gantt_data,
            "summary": {
                "total_duration": (df_cronograma['Fecha_Fin'].max() - df_cronograma['Fecha_Inicio'].min()).days,
                "start_date": df_cronograma['Fecha_Inicio'].min().strftime('%Y-%m-%d'),
                "end_date": df_cronograma['Fecha_Fin'].max().strftime('%Y-%m-%d'),
                "total_activities": len(df_cronograma)
            }
        }
        
        # Guardar el cronograma actual en la instancia
        scheduler.df_actividades = df_cronograma
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_schedule():
    """
    Optimiza el cronograma actual.
    """
    try:
        if scheduler.df_actividades is None:
            return jsonify({"error": "No hay cronograma para optimizar"}), 400
        
        # Optimizar cronograma
        df_optimizado = scheduler.optimizar_cronograma(scheduler.df_actividades)
        
        # Generar nuevo gráfico
        gantt_data = generate_gantt_data(df_optimizado)
        
        # Calcular mejoras
        duracion_original = (scheduler.df_actividades['Fecha_Fin'].max() - 
                           scheduler.df_actividades['Fecha_Inicio'].min()).days
        duracion_optimizada = (df_optimizado['Fecha_Fin'].max() - 
                             df_optimizado['Fecha_Inicio'].min()).days
        mejora = duracion_original - duracion_optimizada
        porcentaje_mejora = (mejora / duracion_original) * 100 if duracion_original > 0 else 0
        
        response = {
            "success": True,
            "activities": df_optimizado.to_dict('records'),
            "gantt_data": gantt_data,
            "optimization": {
                "time_saved": mejora,
                "improvement_percentage": round(porcentaje_mejora, 1),
                "original_duration": duracion_original,
                "optimized_duration": duracion_optimizada
            },
            "summary": {
                "total_duration": duracion_optimizada,
                "start_date": df_optimizado['Fecha_Inicio'].min().strftime('%Y-%m-%d'),
                "end_date": df_optimizado['Fecha_Fin'].max().strftime('%Y-%m-%d'),
                "total_activities": len(df_optimizado)
            }
        }
        
        # Actualizar cronograma
        scheduler.df_actividades = df_optimizado
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Procesa preguntas del chat.
    
    Body JSON:
    {
        "question": "pregunta del usuario"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Pregunta requerida"}), 400
        
        question = data['question']
        
        if scheduler.df_actividades is None:
            return jsonify({
                "success": True,
                "response": "Primero necesito que proceses un proyecto. Describe tu proyecto de construcción o sube un archivo CSV."
            })
        
        # Procesar pregunta
        response = scheduler.responder_pregunta(question, scheduler.df_actividades)
        
        return jsonify({
            "success": True,
            "response": response
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Maneja la carga de archivos CSV/Excel.
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No se encontró archivo"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No se seleccionó archivo"}), 400
        
        if file and allowed_file(file.filename):
            # Guardar archivo temporalmente
            filename = file.filename
            filepath = os.path.join('uploads', filename)
            os.makedirs('uploads', exist_ok=True)
            file.save(filepath)
            
            # Procesar archivo
            df_actividades = scheduler.leer_entrada(filepath)
            df_cronograma = scheduler.generar_cronograma(df_actividades)
            
            # Generar gráfico
            gantt_data = generate_gantt_data(df_cronograma)
            
            # Limpiar archivo temporal
            os.remove(filepath)
            
            response = {
                "success": True,
                "activities": df_cronograma.to_dict('records'),
                "gantt_data": gantt_data,
                "summary": {
                    "total_duration": (df_cronograma['Fecha_Fin'].max() - df_cronograma['Fecha_Inicio'].min()).days,
                    "start_date": df_cronograma['Fecha_Inicio'].min().strftime('%Y-%m-%d'),
                    "end_date": df_cronograma['Fecha_Fin'].max().strftime('%Y-%m-%d'),
                    "total_activities": len(df_cronograma)
                }
            }
            
            # Guardar cronograma
            scheduler.df_actividades = df_cronograma
            
            return jsonify(response)
        
        else:
            return jsonify({"error": "Tipo de archivo no permitido"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Obtiene el estado actual del sistema.
    """
    has_schedule = scheduler.df_actividades is not None
    
    status = {
        "success": True,
        "has_schedule": has_schedule,
        "system_status": "running"
    }
    
    if has_schedule:
        df = scheduler.df_actividades
        status["current_schedule"] = {
            "total_activities": len(df),
            "total_duration": (df['Fecha_Fin'].max() - df['Fecha_Inicio'].min()).days,
            "start_date": df['Fecha_Inicio'].min().strftime('%Y-%m-%d'),
            "end_date": df['Fecha_Fin'].max().strftime('%Y-%m-%d')
        }
    
    return jsonify(status)

@app.route('/api/analyze-risks', methods=['POST'])
def analyze_risks():
    """
    Analiza riesgos del proyecto usando Gemini AI.
    """
    try:
        if scheduler.df_actividades is None:
            return jsonify({"error": "No hay cronograma para analizar"}), 400
        
        # Importar servicio de Gemini
        try:
            from services.gemini_service import get_gemini_service
            gemini_service = get_gemini_service()
            
            if not gemini_service:
                return jsonify({"error": "Gemini no está configurado"}), 500
            
            # Preparar datos para análisis
            actividades = scheduler.df_actividades.to_dict('records')
            
            # Analizar riesgos con Gemini
            analisis_riesgos = gemini_service.analizar_riesgos_proyecto(actividades)
            
            return jsonify({
                "success": True,
                "risk_analysis": analisis_riesgos
            })
            
        except ImportError:
            return jsonify({"error": "Servicio de Gemini no disponible"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai-optimize', methods=['POST'])
def ai_optimize():
    """
    Optimiza el cronograma usando Gemini AI.
    """
    try:
        if scheduler.df_actividades is None:
            return jsonify({"error": "No hay cronograma para optimizar"}), 400
        
        # Importar servicio de Gemini
        try:
            from services.gemini_service import get_gemini_service
            gemini_service = get_gemini_service()
            
            if not gemini_service:
                return jsonify({"error": "Gemini no está configurado"}), 500
            
            # Preparar datos para optimización
            actividades = scheduler.df_actividades.to_dict('records')
            cronograma_actual = {
                "duracion_total": (scheduler.df_actividades['Fecha_Fin'].max() - scheduler.df_actividades['Fecha_Inicio'].min()).days,
                "fecha_inicio": scheduler.df_actividades['Fecha_Inicio'].min().strftime('%Y-%m-%d'),
                "fecha_fin": scheduler.df_actividades['Fecha_Fin'].max().strftime('%Y-%m-%d')
            }
            
            # Optimizar con Gemini
            optimizacion_ia = gemini_service.optimizar_cronograma(actividades, cronograma_actual)
            
            return jsonify({
                "success": True,
                "ai_optimization": optimizacion_ia
            })
            
        except ImportError:
            return jsonify({"error": "Servicio de Gemini no disponible"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_gantt_data(df):
    """
    Genera datos para el gráfico de Gantt en formato JSON.
    """
    gantt_data = []
    
    for _, row in df.iterrows():
        gantt_data.append({
            "task": row['Actividad'],
            "start": row['Fecha_Inicio'].strftime('%Y-%m-%d'),
            "end": row['Fecha_Fin'].strftime('%Y-%m-%d'),
            "duration": row['Duración'],
            "predecessors": row['Predecesoras']
        })
    
    return gantt_data

def allowed_file(filename):
    """
    Verifica si el tipo de archivo está permitido.
    """
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    # Crear directorio de uploads si no existe
    os.makedirs('uploads', exist_ok=True)
    
    # Ejecutar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
