import React from 'react';
import { Calendar, Clock, Users, Zap, TrendingUp, Target } from 'lucide-react';

const ProjectSummary = ({ summary, optimization, onOptimize }) => {
  if (!summary) return null;

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="space-y-6">
      {/* Header con botón de optimización */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">📊 Resumen del Proyecto</h2>
          <p className="text-white/80">Información general del cronograma generado</p>
        </div>
        
        <button
          onClick={onOptimize}
          className="btn-secondary text-white px-6 py-3 rounded-lg font-medium flex items-center space-x-2 hover:shadow-lg transition-all"
        >
          <Zap className="h-5 w-5" />
          <span>Optimizar Cronograma</span>
        </button>
      </div>

      {/* Optimización aplicada */}
      {optimization && (
        <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl p-6 text-white">
          <div className="flex items-center space-x-3 mb-4">
            <TrendingUp className="h-6 w-6" />
            <h3 className="text-lg font-semibold">¡Optimización Aplicada!</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white/20 rounded-lg p-4">
              <p className="text-sm opacity-90">Tiempo Ahorrado</p>
              <p className="text-2xl font-bold">{optimization.time_saved} días</p>
            </div>
            
            <div className="bg-white/20 rounded-lg p-4">
              <p className="text-sm opacity-90">Mejora</p>
              <p className="text-2xl font-bold">{optimization.improvement_percentage}%</p>
            </div>
            
            <div className="bg-white/20 rounded-lg p-4">
              <p className="text-sm opacity-90">Duración Anterior</p>
              <p className="text-2xl font-bold">{optimization.original_duration} días</p>
            </div>
          </div>
        </div>
      )}

      {/* Estadísticas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Duración Total */}
        <div className="card rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Clock className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-800">Duración Total</h3>
          </div>
          <p className="text-3xl font-bold text-blue-600 mb-1">
            {summary.total_duration}
          </p>
          <p className="text-sm text-gray-600">días</p>
        </div>

        {/* Total de Actividades */}
        <div className="card rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Users className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-800">Actividades</h3>
          </div>
          <p className="text-3xl font-bold text-purple-600 mb-1">
            {summary.total_activities}
          </p>
          <p className="text-sm text-gray-600">tareas</p>
        </div>

        {/* Fecha de Inicio */}
        <div className="card rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <Calendar className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-800">Fecha de Inicio</h3>
          </div>
          <p className="text-lg font-bold text-green-600 mb-1">
            {formatDate(summary.start_date)}
          </p>
          <p className="text-sm text-gray-600">inicio del proyecto</p>
        </div>

        {/* Fecha de Fin */}
        <div className="card rounded-xl p-6">
          <div className="flex items-center space-x-3 mb-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Target className="h-6 w-6 text-orange-600" />
            </div>
            <h3 className="font-semibold text-gray-800">Fecha de Fin</h3>
          </div>
          <p className="text-lg font-bold text-orange-600 mb-1">
            {formatDate(summary.end_date)}
          </p>
          <p className="text-sm text-gray-600">finalización estimada</p>
        </div>
      </div>

      {/* Timeline visual */}
      <div className="card rounded-xl p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">📅 Timeline del Proyecto</h3>
        
        <div className="relative">
          {/* Línea de tiempo */}
          <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>
          
          {/* Puntos de inicio y fin */}
          <div className="relative space-y-4">
            <div className="flex items-center space-x-4">
              <div className="relative z-10 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <div className="w-3 h-3 bg-white rounded-full"></div>
              </div>
              <div>
                <p className="font-medium text-gray-800">Inicio del Proyecto</p>
                <p className="text-sm text-gray-600">{formatDate(summary.start_date)}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="relative z-10 w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                <div className="w-3 h-3 bg-white rounded-full"></div>
              </div>
              <div>
                <p className="font-medium text-gray-800">Finalización del Proyecto</p>
                <p className="text-sm text-gray-600">{formatDate(summary.end_date)}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectSummary;
