import React from 'react';
import Plot from 'react-plotly.js';

const GanttChart = ({ data }) => {
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

  // Preparar datos para Plotly
  const traces = data.map((task, index) => {
    const startDate = new Date(task.start);
    const endDate = new Date(task.end);
    
    return {
      x: [startDate, endDate],
      y: [task.task, task.task],
      mode: 'lines+markers',
      line: {
        color: `hsl(${(index * 137.5) % 360}, 70%, 50%)`,
        width: 20
      },
      marker: {
        size: 8,
        color: `hsl(${(index * 137.5) % 360}, 70%, 50%)`
      },
      name: task.task,
      hovertemplate: `
        <b>${task.task}</b><br>
        Inicio: ${startDate.toLocaleDateString('es-ES')}<br>
        Fin: ${endDate.toLocaleDateString('es-ES')}<br>
        Duración: ${task.duration} días<br>
        Predecesoras: ${task.predecessors || 'Ninguna'}
        <extra></extra>
      `,
      showlegend: false
    };
  });

  const layout = {
    title: {
      text: '📅 Cronograma de Construcción - Diagrama de Gantt',
      font: { size: 20, color: '#2d3748' },
      x: 0.5,
      xanchor: 'center'
    },
    xaxis: {
      title: 'Fecha',
      tickformat: '%d/%m/%Y',
      tickangle: 45,
      gridcolor: '#e2e8f0',
      showgrid: true
    },
    yaxis: {
      title: 'Actividades',
      categoryorder: 'category ascending',
      gridcolor: '#e2e8f0',
      showgrid: true
    },
    height: Math.max(400, data.length * 50 + 200),
    margin: {
      l: 200,
      r: 50,
      t: 80,
      b: 100
    },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    font: {
      family: 'Inter, sans-serif',
      size: 12,
      color: '#2d3748'
    },
    hovermode: 'closest'
  };

  const config = {
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    responsive: true
  };

  return (
    <div className="p-6">
      <Plot
        data={traces}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
      />
      
      {/* Información adicional */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded-lg p-4">
          <h4 className="font-semibold text-blue-800 mb-2">📊 Estadísticas</h4>
          <p className="text-sm text-blue-600">
            Total de actividades: <span className="font-medium">{data.length}</span>
          </p>
        </div>
        
        <div className="bg-green-50 rounded-lg p-4">
          <h4 className="font-semibold text-green-800 mb-2">⏱️ Duración</h4>
          <p className="text-sm text-green-600">
            Duración total: <span className="font-medium">
              {Math.max(...data.map(task => 
                Math.ceil((new Date(task.end) - new Date(task.start)) / (1000 * 60 * 60 * 24))
              ))} días
            </span>
          </p>
        </div>
        
        <div className="bg-purple-50 rounded-lg p-4">
          <h4 className="font-semibold text-purple-800 mb-2">🔗 Dependencias</h4>
          <p className="text-sm text-purple-600">
            Actividades con predecesoras: <span className="font-medium">
              {data.filter(task => task.predecessors && task.predecessors.trim()).length}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default GanttChart;
