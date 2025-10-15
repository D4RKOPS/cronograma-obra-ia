import React from 'react';
import { Brain, Lightbulb, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';

const GeminiAnalysis = ({ analysis, optimization }) => {
  if (!analysis && !optimization) {
    return null;
  }

  return (
    <div className="space-y-4 mb-6">
      {/* Análisis del Proyecto */}
      {analysis && (
        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-500">
          <div className="flex items-start space-x-3">
            <Brain className="h-6 w-6 text-blue-600 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-bold text-gray-800 mb-2">
                🤖 Análisis de IA - Gemini
              </h3>
              <div className="text-gray-700 space-y-2">
                {typeof analysis === 'string' ? (
                  <p className="leading-relaxed">{analysis}</p>
                ) : (
                  <>
                    {analysis.resumen && (
                      <div className="bg-blue-50 rounded-lg p-3 mb-3">
                        <p className="text-sm font-medium text-blue-900">{analysis.resumen}</p>
                      </div>
                    )}
                    
                    {analysis.insights && analysis.insights.length > 0 && (
                      <div>
                        <h4 className="font-semibold text-gray-800 mb-2 flex items-center">
                          <Lightbulb className="h-4 w-4 mr-2 text-yellow-600" />
                          Observaciones clave:
                        </h4>
                        <ul className="space-y-1">
                          {analysis.insights.map((insight, idx) => (
                            <li key={idx} className="text-sm text-gray-600 flex items-start">
                              <span className="text-blue-500 mr-2">•</span>
                              <span>{insight}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {analysis.riesgos && analysis.riesgos.length > 0 && (
                      <div className="mt-3">
                        <h4 className="font-semibold text-gray-800 mb-2 flex items-center">
                          <AlertTriangle className="h-4 w-4 mr-2 text-orange-600" />
                          Riesgos identificados:
                        </h4>
                        <ul className="space-y-1">
                          {analysis.riesgos.map((riesgo, idx) => (
                            <li key={idx} className="text-sm text-orange-700 flex items-start bg-orange-50 p-2 rounded">
                              <span className="text-orange-500 mr-2">⚠️</span>
                              <span>{riesgo}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {analysis.recomendaciones && analysis.recomendaciones.length > 0 && (
                      <div className="mt-3">
                        <h4 className="font-semibold text-gray-800 mb-2 flex items-center">
                          <CheckCircle className="h-4 w-4 mr-2 text-green-600" />
                          Recomendaciones:
                        </h4>
                        <ul className="space-y-1">
                          {analysis.recomendaciones.map((rec, idx) => (
                            <li key={idx} className="text-sm text-green-700 flex items-start bg-green-50 p-2 rounded">
                              <span className="text-green-500 mr-2">✓</span>
                              <span>{rec}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Análisis de Optimización */}
      {optimization && (
        <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-500">
          <div className="flex items-start space-x-3">
            <TrendingUp className="h-6 w-6 text-green-600 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-lg font-bold text-gray-800 mb-2">
                ⚡ Optimización Aplicada
              </h3>
              
              {optimization.explicacion && (
                <div className="bg-green-50 rounded-lg p-4 mb-3">
                  <p className="text-sm text-green-900 leading-relaxed">
                    {optimization.explicacion}
                  </p>
                </div>
              )}

              {optimization.cambios && optimization.cambios.length > 0 && (
                <div className="mb-3">
                  <h4 className="font-semibold text-gray-800 mb-2">Cambios realizados:</h4>
                  <ul className="space-y-2">
                    {optimization.cambios.map((cambio, idx) => (
                      <li key={idx} className="text-sm text-gray-700 flex items-start bg-white p-2 rounded border border-gray-200">
                        <span className="text-green-500 mr-2 font-bold">→</span>
                        <span>{cambio}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {optimization.mejoras && (
                <div className="grid grid-cols-2 gap-3 mt-3">
                  {optimization.mejoras.tiempo && (
                    <div className="bg-blue-50 rounded-lg p-3">
                      <div className="text-xs text-blue-600 font-medium">Tiempo ahorrado</div>
                      <div className="text-2xl font-bold text-blue-700">
                        {optimization.mejoras.tiempo}
                      </div>
                    </div>
                  )}
                  {optimization.mejoras.porcentaje && (
                    <div className="bg-purple-50 rounded-lg p-3">
                      <div className="text-xs text-purple-600 font-medium">Mejora</div>
                      <div className="text-2xl font-bold text-purple-700">
                        {optimization.mejoras.porcentaje}%
                      </div>
                    </div>
                  )}
                </div>
              )}

              {optimization.razon && (
                <div className="mt-3 bg-gray-50 rounded-lg p-3">
                  <p className="text-xs text-gray-600 font-medium mb-1">¿Por qué funciona?</p>
                  <p className="text-sm text-gray-700">{optimization.razon}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GeminiAnalysis;

