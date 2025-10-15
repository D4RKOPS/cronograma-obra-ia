import React, { useState } from 'react';
import { Calendar, Clock, Users, Download, ChevronDown, ChevronUp } from 'lucide-react';

const SimpleGanttChart = ({ data }) => {
  const [showAll, setShowAll] = useState(false);
  const [isExporting, setIsExporting] = useState(false);

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        <div className="text-center">
          <div className="text-4xl mb-2">📊</div>
          <p>No hay datos para mostrar</p>
        </div>
      </div>
    );
  }

  // Función para exportar a CSV
  const exportToCSV = () => {
    setIsExporting(true);
    
    try {
      // Crear contenido CSV
      const headers = ['Actividad', 'Duración (días)', 'Fecha Inicio', 'Fecha Fin', 'Predecesoras'];
      const rows = data.map(task => [
        `"${task.task}"`,
        task.duration,
        new Date(task.start).toLocaleDateString('es-ES'),
        new Date(task.end).toLocaleDateString('es-ES'),
        `"${task.predecessors || ''}"`
      ]);

      const csvContent = [
        headers.join(','),
        ...rows.map(row => row.join(','))
      ].join('\n');

      // Crear y descargar archivo
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      
      link.setAttribute('href', url);
      link.setAttribute('download', `cronograma_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      setTimeout(() => setIsExporting(false), 1000);
    } catch (error) {
      console.error('Error al exportar:', error);
      setIsExporting(false);
      alert('Error al exportar el cronograma');
    }
  };

  // Calcular el rango de fechas
  const startDate = new Date(Math.min(...data.map(task => new Date(task.start))));
  const endDate = new Date(Math.max(...data.map(task => new Date(task.end))));
  const totalDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));

  // Función para calcular la posición y ancho de cada barra
  const getTaskPosition = (task) => {
    const taskStart = new Date(task.start);
    const taskEnd = new Date(task.end);
    const startOffset = Math.ceil((taskStart - startDate) / (1000 * 60 * 60 * 24));
    const duration = Math.ceil((taskEnd - taskStart) / (1000 * 60 * 60 * 24));
    
    return {
      left: `${(startOffset / totalDays) * 100}%`,
      width: `${(duration / totalDays) * 100}%`
    };
  };

  // Colores para las barras
  const colors = [
    'bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-orange-500',
    'bg-pink-500', 'bg-indigo-500', 'bg-red-500', 'bg-yellow-500',
    'bg-teal-500', 'bg-cyan-500'
  ];

  // Determinar cuántas actividades mostrar
  const displayedData = showAll ? data : data.slice(0, 20);

  return (
    <div className="p-6">
      {/* Timeline Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">📅 Cronograma de Construcción</h3>
          
          {/* Botón de Exportar */}
          <button
            onClick={exportToCSV}
            disabled={isExporting}
            className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Download className="h-4 w-4" />
            <span>{isExporting ? 'Exportando...' : 'Exportar CSV'}</span>
          </button>
        </div>
        
        {/* Timeline con fechas */}
        <div className="relative bg-gray-100 rounded-lg p-4 mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>{startDate.toLocaleDateString('es-ES')}</span>
            <span>{endDate.toLocaleDateString('es-ES')}</span>
          </div>
          
          {/* Línea de tiempo */}
          <div className="relative h-2 bg-gray-200 rounded-full">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full"></div>
          </div>
          
          <div className="text-center text-sm text-gray-500 mt-2">
            {totalDays} días de duración total
          </div>
        </div>
      </div>

      {/* Gantt Chart */}
      <div className="space-y-3 max-h-[600px] overflow-y-auto overflow-x-auto">
        {displayedData.map((task, index) => {
          const position = getTaskPosition(task);
          const color = colors[index % colors.length];
          const widthPercent = parseFloat(position.width);
          const isSmallBar = widthPercent < 5; // Barras menores al 5% del ancho total
          
          return (
            <div key={index} className="flex items-center space-x-3 hover:bg-gray-50 p-2 rounded-lg transition-colors min-w-max">
              {/* Nombre de la tarea */}
              <div className="w-52 text-sm font-medium text-gray-700 flex-shrink-0">
                <div className="truncate" title={task.task}>
                  {task.task}
                </div>
                <div className="text-xs text-gray-500">
                  {task.duration} días
                </div>
              </div>
              
              {/* Barra de progreso */}
              <div className="flex-1 relative min-w-[400px]">
                <div className="h-10 bg-gray-200 rounded-lg relative overflow-visible">
                  <div
                    className={`absolute top-0 h-full ${color} rounded-lg flex items-center shadow-md hover:shadow-lg transition-shadow`}
                    style={{
                      left: position.left,
                      width: isSmallBar ? '5%' : position.width,
                      minWidth: '40px'
                    }}
                  >
                    {/* Contenido de la barra */}
                    <div className="w-full px-2 flex items-center justify-between">
                      <span className="text-white text-xs font-bold truncate">
                        {task.duration}d
                      </span>
                    </div>
                    
                    {/* Tooltip con información detallada */}
                    <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 bg-gray-800 text-white text-xs px-3 py-2 rounded whitespace-nowrap opacity-0 hover:opacity-100 transition-opacity z-10 shadow-lg">
                      <div className="font-semibold mb-1">{task.task}</div>
                      <div>⏱️ Duración: {task.duration} días</div>
                      <div>📅 Inicio: {new Date(task.start).toLocaleDateString('es-ES')}</div>
                      <div>🏁 Fin: {new Date(task.end).toLocaleDateString('es-ES')}</div>
                      {task.predecessors && task.predecessors.trim() && (
                        <div className="mt-1 pt-1 border-t border-gray-600">
                          <div className="text-blue-300">
                            {task.predecessors} → {task.task}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                
                {/* Fechas */}
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>{new Date(task.start).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' })}</span>
                  <span>{new Date(task.end).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' })}</span>
                </div>
              </div>
              
              {/* Información adicional - Dependencias con flechas */}
              <div className="w-72 text-xs flex-shrink-0">
                {task.predecessors && task.predecessors.trim() ? (
                  <div className="bg-blue-50 px-3 py-2 rounded-lg border border-blue-200">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-blue-700 font-semibold whitespace-nowrap">
                        {task.predecessors}
                      </span>
                      <span className="text-blue-400 font-bold text-base flex-shrink-0">→</span>
                      <span className="text-gray-800 font-semibold whitespace-nowrap">
                        {task.task}
                      </span>
                    </div>
                  </div>
                ) : (
                  <div className="bg-green-50 px-3 py-2 rounded-lg border border-green-200">
                    <div className="flex items-center gap-2 text-green-700">
                      <span className="text-base">⭐</span>
                      <span className="font-semibold whitespace-nowrap">Inicio del Proyecto</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Botón Mostrar Más / Mostrar Menos */}
      {data.length > 20 && (
        <div className="mt-4 text-center">
          <button
            onClick={() => setShowAll(!showAll)}
            className="inline-flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
          >
            {showAll ? (
              <>
                <ChevronUp className="h-5 w-5" />
                <span>Mostrar menos</span>
              </>
            ) : (
              <>
                <ChevronDown className="h-5 w-5" />
                <span>Mostrar todas las actividades ({data.length - 20} más)</span>
              </>
            )}
          </button>
          
          {!showAll && (
            <p className="text-sm text-gray-500 mt-2">
              Mostrando 20 de {data.length} actividades
            </p>
          )}
        </div>
      )}

      {/* Información adicional */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Users className="h-5 w-5 text-blue-600" />
            <h4 className="font-semibold text-blue-800">Estadísticas</h4>
          </div>
          <p className="text-sm text-blue-600">
            Total de actividades: <span className="font-medium">{data.length}</span>
          </p>
        </div>
        
        <div className="bg-green-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Clock className="h-5 w-5 text-green-600" />
            <h4 className="font-semibold text-green-800">Duración</h4>
          </div>
          <p className="text-sm text-green-600">
            Duración total: <span className="font-medium">{totalDays} días</span>
          </p>
        </div>
        
        <div className="bg-purple-50 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Calendar className="h-5 w-5 text-purple-600" />
            <h4 className="font-semibold text-purple-800">Dependencias</h4>
          </div>
          <p className="text-sm text-purple-600">
            Con predecesoras: <span className="font-medium">
              {data.filter(task => task.predecessors && task.predecessors.trim()).length}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SimpleGanttChart;
