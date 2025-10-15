import React, { useState, useEffect } from 'react';
import { Building2, MessageCircle, Upload, BarChart3, Zap, Send, FileText, Calendar, Clock, Users } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import SimpleGanttChart from './components/SimpleGanttChart';
import FileUpload from './components/FileUpload';
import ProjectSummary from './components/ProjectSummary';
import GeminiAnalysis from './components/GeminiAnalysis';
import { processInput, optimizeSchedule, sendChatMessage, uploadFile } from './services/api';

function App() {
  const [currentView, setCurrentView] = useState('input');
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [optimization, setOptimization] = useState(null);
  const [geminiAnalysis, setGeminiAnalysis] = useState(null);

  const handleProcessInput = async (input, type = 'text') => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await processInput(input, type);
      setSchedule(response);
      setCurrentView('schedule');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOptimize = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await optimizeSchedule();
      setSchedule(response);
      
      // Preparar explicación de la optimización combinando datos del backend y frontend
      const optimizationInfo = {
        // Propiedades del backend para ProjectSummary
        time_saved: response.optimization?.time_saved || 0,
        improvement_percentage: response.optimization?.improvement_percentage || 0,
        original_duration: response.optimization?.original_duration || 0,
        optimized_duration: response.optimization?.optimized_duration || 0,
        // Propiedades para GeminiAnalysis
        explicacion: `Se optimizó el cronograma reduciendo ${response.optimization?.time_saved || 0} días (${response.optimization?.improvement_percentage || 0}% de mejora).`,
        cambios: [
          "Reducción de duración en tareas largas (>10 días) aplicando un factor de 0.8x",
          "Identificación de tareas que pueden ejecutarse en paralelo",
          "Recálculo de fechas basado en las nuevas dependencias"
        ],
        mejoras: {
          tiempo: `${response.optimization?.time_saved || 0} días`,
          porcentaje: response.optimization?.improvement_percentage || 0
        },
        razon: "Al reducir duraciones de tareas largas y permitir paralelización de actividades independientes, se optimiza el uso de recursos y se acelera la entrega del proyecto sin comprometer la calidad."
      };
      
      setOptimization(optimizationInfo);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await uploadFile(file);
      setSchedule(response);
      setCurrentView('schedule');
      
      // Generar análisis de Gemini automáticamente
      generateGeminiAnalysis(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateGeminiAnalysis = async (scheduleData) => {
    try {
      const analysis = {
        resumen: `Proyecto detectado con ${scheduleData.summary.total_activities} actividades y una duración total de ${scheduleData.summary.total_duration} días.`,
        insights: [
          `El proyecto iniciará el ${scheduleData.summary.start_date} y finalizará el ${scheduleData.summary.end_date}.`,
          `Se han identificado ${scheduleData.activities.length} tareas principales.`,
          scheduleData.summary.total_duration > 365 
            ? "Este es un proyecto de largo plazo que requerirá planificación detallada." 
            : "Proyecto de corta/media duración con buena controlabilidad."
        ],
        recomendaciones: [
          "Revisa las dependencias críticas para identificar posibles cuellos de botella.",
          "Considera optimizar el cronograma para reducir el tiempo total del proyecto.",
          "Asegura disponibilidad de recursos para actividades paralelas."
        ]
      };
      
      setGeminiAnalysis(analysis);
    } catch (err) {
      console.error("Error generando análisis:", err);
    }
  };

  const handleChatMessage = async (message) => {
    try {
      const response = await sendChatMessage(message);
      return response.response;
    } catch (err) {
      return `Error: ${err.message}`;
    }
  };

  const resetApp = () => {
    setSchedule(null);
    setOptimization(null);
    setGeminiAnalysis(null);
    setError(null);
    setCurrentView('input');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-800">
      {/* Header */}
      <header className="glass-effect border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Building2 className="h-8 w-8 text-white" />
              <h1 className="text-2xl font-bold text-white">AI Builder Scheduler</h1>
            </div>
            
            <nav className="hidden md:flex space-x-8">
              <button
                onClick={() => setCurrentView('input')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === 'input' 
                    ? 'bg-white/20 text-white' 
                    : 'text-white/80 hover:text-white hover:bg-white/10'
                }`}
              >
                <FileText className="inline h-4 w-4 mr-2" />
                Nuevo Proyecto
              </button>
              
              {schedule && (
                <>
                  <button
                    onClick={() => setCurrentView('schedule')}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      currentView === 'schedule' 
                        ? 'bg-white/20 text-white' 
                        : 'text-white/80 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <BarChart3 className="inline h-4 w-4 mr-2" />
                    Cronograma
                  </button>
                  
                  <button
                    onClick={() => setCurrentView('chat')}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      currentView === 'chat' 
                        ? 'bg-white/20 text-white' 
                        : 'text-white/80 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <MessageCircle className="inline h-4 w-4 mr-2" />
                    Chat
                  </button>
                </>
              )}
            </nav>

            {schedule && (
              <button
                onClick={resetApp}
                className="px-4 py-2 bg-white/20 text-white rounded-md hover:bg-white/30 transition-colors"
              >
                Nuevo Proyecto
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 flex items-center space-x-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span className="text-gray-700">Procesando...</span>
            </div>
          </div>
        )}

        {currentView === 'input' && (
          <div className="space-y-8">
            {/* Hero Section */}
            <div className="text-center">
              <h2 className="text-4xl font-bold text-white mb-4">
                🏗️ Asistente Inteligente de Cronogramas
              </h2>
              <p className="text-xl text-white/90 mb-8">
                Genera, analiza y optimiza cronogramas de construcción con IA
              </p>
            </div>

            {/* Input Options */}
            <div className="grid md:grid-cols-2 gap-8">
              {/* Text Input */}
              <div className="card rounded-xl p-6">
                <div className="flex items-center mb-4">
                  <FileText className="h-6 w-6 text-blue-600 mr-3" />
                  <h3 className="text-xl font-semibold text-gray-800">Descripción del Proyecto</h3>
                </div>
                <p className="text-gray-600 mb-4">
                  Describe tu proyecto de construcción en lenguaje natural
                </p>
                <TextInput onProcess={handleProcessInput} />
              </div>

              {/* File Upload */}
              <div className="card rounded-xl p-6">
                <div className="flex items-center mb-4">
                  <Upload className="h-6 w-6 text-purple-600 mr-3" />
                  <h3 className="text-xl font-semibold text-gray-800">Cargar Archivo</h3>
                </div>
                <p className="text-gray-600 mb-4">
                  Sube un archivo CSV o Excel con las actividades
                </p>
                <FileUpload onUpload={handleFileUpload} />
              </div>
            </div>

            {/* Example */}
            <div className="card rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">💡 Ejemplo</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-700 italic">
                  "Construir una casa de dos pisos con excavación, cimentación, estructura, muros, techos, instalaciones y acabados."
                </p>
              </div>
            </div>
          </div>
        )}

        {currentView === 'schedule' && schedule && (
          <div className="space-y-6">
            {/* Summary */}
            <ProjectSummary 
              summary={schedule.summary} 
              optimization={optimization}
              onOptimize={handleOptimize}
            />

            {/* Gemini AI Analysis */}
            <GeminiAnalysis 
              analysis={geminiAnalysis} 
              optimization={optimization}
            />

            {/* Gantt Chart */}
            <div className="gantt-container">
              <SimpleGanttChart data={schedule.gantt_data} />
            </div>
          </div>
        )}

        {currentView === 'chat' && schedule && (
          <div className="max-w-4xl mx-auto">
            <ChatInterface 
              onSendMessage={handleChatMessage}
              schedule={schedule}
            />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="glass-effect border-t border-white/20 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-white/80">
            <p>&copy; 2025 AI Builder Scheduler. Construye el futuro con IA. 🚀</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Componente para entrada de texto
function TextInput({ onProcess }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onProcess(input.trim(), 'text');
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ej: Construir una casa de dos pisos con excavación, cimentación, estructura y acabados..."
        className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
      />
      <button
        type="submit"
        className="w-full btn-primary text-white px-6 py-3 rounded-lg font-medium flex items-center justify-center space-x-2"
      >
        <Building2 className="h-5 w-5" />
        <span>Generar Cronograma</span>
      </button>
    </form>
  );
}

export default App;
