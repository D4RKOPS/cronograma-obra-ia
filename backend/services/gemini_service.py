#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicio de integración con Google Gemini API
============================================

Este módulo proporciona funciones para interactuar con Google Gemini
para análisis de texto, generación de cronogramas y optimización de proyectos.
"""

import google.generativeai as genai
import os
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GeminiService:
    """
    Servicio para interactuar con Google Gemini API.
    """
    
    def __init__(self):
        """Inicializa el servicio de Gemini."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en las variables de entorno")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Configuración de seguridad
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    
    def analizar_proyecto_construccion(self, descripcion: str) -> Dict[str, Any]:
        """
        Analiza una descripción de proyecto de construcción y extrae actividades, duraciones y dependencias.
        
        Args:
            descripcion (str): Descripción del proyecto en lenguaje natural
            
        Returns:
            Dict[str, Any]: Diccionario con actividades extraídas
        """
        prompt = f"""
Eres un experto en gestión de proyectos de construcción. Analiza la siguiente descripción de proyecto y extrae las actividades, duraciones estimadas y dependencias.

Descripción del proyecto: "{descripcion}"

Por favor, devuelve la información en formato JSON con la siguiente estructura:
{{
    "actividades": [
        {{
            "Actividad": "Nombre de la actividad",
            "Duración": número_de_días,
            "Predecesoras": "nombre_de_actividad_predecesora o vacío si no tiene"
        }}
    ],
    "analisis": "Breve análisis del proyecto y recomendaciones"
}}

Reglas importantes:
1. Estima duraciones realistas basadas en el tipo de actividad
2. Identifica dependencias lógicas entre actividades
3. Si no se especifican dependencias, infiérelas lógicamente
4. Usa nombres de actividades claros y específicos
5. Devuelve SOLO el JSON, sin texto adicional

Ejemplo de respuesta:
{{
    "actividades": [
        {{
            "Actividad": "Excavación",
            "Duración": 5,
            "Predecesoras": ""
        }},
        {{
            "Actividad": "Cimentación",
            "Duración": 10,
            "Predecesoras": "Excavación"
        }}
    ],
    "analisis": "Proyecto de construcción estándar con secuencia lógica de actividades."
}}
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            # Limpiar la respuesta y extraer JSON
            response_text = response.text.strip()
            
            # Buscar el JSON en la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No se pudo extraer JSON de la respuesta")
                
        except Exception as e:
            print(f"Error al analizar proyecto con Gemini: {e}")
            return {
                "actividades": [],
                "analisis": f"Error al procesar con IA: {str(e)}"
            }
    
    def optimizar_cronograma(self, actividades: List[Dict], cronograma_actual: Dict) -> Dict[str, Any]:
        """
        Optimiza un cronograma existente usando IA.
        
        Args:
            actividades (List[Dict]): Lista de actividades del proyecto
            cronograma_actual (Dict): Cronograma actual con fechas
            
        Returns:
            Dict[str, Any]: Recomendaciones de optimización
        """
        prompt = f"""
Eres un experto en optimización de cronogramas de construcción. Analiza el siguiente cronograma y proporciona recomendaciones de optimización.

Actividades del proyecto:
{json.dumps(actividades, indent=2, ensure_ascii=False)}

Cronograma actual:
{json.dumps(cronograma_actual, indent=2, ensure_ascii=False)}

Por favor, proporciona recomendaciones en formato JSON:
{{
    "recomendaciones": [
        {{
            "tipo": "paralelizacion|reduccion_duracion|reorganizacion",
            "descripcion": "Descripción detallada de la recomendación",
            "actividades_afectadas": ["actividad1", "actividad2"],
            "ahorro_estimado": número_de_días,
            "riesgo": "bajo|medio|alto"
        }}
    ],
    "analisis_general": "Análisis general del cronograma y oportunidades de mejora",
    "duracion_optimizada": número_de_días_estimado
}}

Enfócate en:
1. Identificar actividades que pueden ejecutarse en paralelo
2. Sugerir reducciones de duración realistas
3. Reorganizar secuencias para mayor eficiencia
4. Evaluar riesgos de cada recomendación
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            response_text = response.text.strip()
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No se pudo extraer JSON de la respuesta")
                
        except Exception as e:
            print(f"Error al optimizar cronograma con Gemini: {e}")
            return {
                "recomendaciones": [],
                "analisis_general": f"Error al procesar con IA: {str(e)}",
                "duracion_optimizada": 0
            }
    
    def responder_pregunta_cronograma(self, pregunta: str, contexto: Dict) -> str:
        """
        Responde preguntas sobre el cronograma usando IA.
        
        Args:
            pregunta (str): Pregunta del usuario
            contexto (Dict): Contexto del proyecto y cronograma
            
        Returns:
            str: Respuesta generada por IA
        """
        prompt = f"""
Eres un asistente experto en gestión de proyectos de construcción. Responde la siguiente pregunta sobre el cronograma del proyecto.

Pregunta: "{pregunta}"

Contexto del proyecto:
{json.dumps(contexto, indent=2, ensure_ascii=False)}

Proporciona una respuesta clara, útil y específica. Incluye:
1. Respuesta directa a la pregunta
2. Explicación técnica si es necesario
3. Recomendaciones prácticas
4. Consideraciones de riesgo si aplica

Mantén la respuesta en español y sé conciso pero informativo.
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"Error al responder pregunta con Gemini: {e}")
            return f"Lo siento, no pude procesar tu pregunta en este momento. Error: {str(e)}"
    
    def analizar_riesgos_proyecto(self, actividades: List[Dict]) -> Dict[str, Any]:
        """
        Analiza riesgos potenciales del proyecto.
        
        Args:
            actividades (List[Dict]): Lista de actividades del proyecto
            
        Returns:
            Dict[str, Any]: Análisis de riesgos
        """
        prompt = f"""
Eres un experto en gestión de riesgos de proyectos de construcción. Analiza los siguientes riesgos potenciales:

Actividades del proyecto:
{json.dumps(actividades, indent=2, ensure_ascii=False)}

Proporciona un análisis de riesgos en formato JSON:
{{
    "riesgos": [
        {{
            "tipo": "técnico|climático|logístico|recursos|tiempo",
            "descripcion": "Descripción del riesgo",
            "probabilidad": "baja|media|alta",
            "impacto": "bajo|medio|alto",
            "mitigacion": "Estrategia de mitigación recomendada"
        }}
    ],
    "resumen": "Resumen general de los principales riesgos identificados"
}}
"""
        
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            response_text = response.text.strip()
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No se pudo extraer JSON de la respuesta")
                
        except Exception as e:
            print(f"Error al analizar riesgos con Gemini: {e}")
            return {
                "riesgos": [],
                "resumen": f"Error al procesar con IA: {str(e)}"
            }

# Instancia global del servicio
gemini_service = None

def get_gemini_service() -> Optional[GeminiService]:
    """
    Obtiene la instancia del servicio de Gemini.
    
    Returns:
        Optional[GeminiService]: Instancia del servicio o None si no está configurado
    """
    global gemini_service
    
    if gemini_service is None:
        try:
            gemini_service = GeminiService()
        except ValueError as e:
            print(f"Gemini no configurado: {e}")
            return None
    
    return gemini_service
