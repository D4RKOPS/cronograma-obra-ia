import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, CheckCircle, AlertCircle } from 'lucide-react';

const FileUpload = ({ onUpload }) => {
  const [uploadStatus, setUploadStatus] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setIsUploading(true);
    setUploadStatus(null);

    try {
      await onUpload(file);
      setUploadStatus('success');
    } catch (error) {
      setUploadStatus('error');
      console.error('Error uploading file:', error);
    } finally {
      setIsUploading(false);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  });

  const getStatusIcon = () => {
    if (uploadStatus === 'success') {
      return <CheckCircle className="h-8 w-8 text-green-500" />;
    }
    if (uploadStatus === 'error') {
      return <AlertCircle className="h-8 w-8 text-red-500" />;
    }
    return <Upload className="h-8 w-8 text-gray-400" />;
  };

  const getStatusMessage = () => {
    if (uploadStatus === 'success') {
      return 'Archivo procesado exitosamente';
    }
    if (uploadStatus === 'error') {
      return 'Error al procesar el archivo';
    }
    return null;
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`upload-area rounded-lg p-8 text-center cursor-pointer transition-all duration-200 ${
          isDragActive ? 'dragover' : ''
        } ${uploadStatus === 'success' ? 'border-green-300 bg-green-50' : ''} ${
          uploadStatus === 'error' ? 'border-red-300 bg-red-50' : ''
        }`}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          {getStatusIcon()}
          
          {isUploading ? (
            <div className="space-y-2">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
              <p className="text-sm text-gray-600">Procesando archivo...</p>
            </div>
          ) : (
            <>
              <div>
                <p className="text-lg font-medium text-gray-700 mb-2">
                  {isDragActive ? 'Suelta el archivo aquí' : 'Arrastra tu archivo aquí'}
                </p>
                <p className="text-sm text-gray-500">
                  o haz clic para seleccionar
                </p>
              </div>
              
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <File className="h-4 w-4" />
                <span>CSV, XLS, XLSX (máx. 10MB)</span>
              </div>
            </>
          )}
        </div>
      </div>

      {getStatusMessage() && (
        <div
          className={`text-center text-sm font-medium ${
            uploadStatus === 'success' ? 'text-green-600' : 'text-red-600'
          }`}
        >
          {getStatusMessage()}
        </div>
      )}

      {/* Ejemplo de formatos */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="font-medium text-gray-700 mb-3">📋 Formatos soportados:</h4>
        
        <div className="space-y-4">
          {/* Formato 1 */}
          <div>
            <p className="text-sm font-medium text-gray-700 mb-1">
              <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded text-xs mr-2">Formato 1</span>
              Estándar (Recomendado)
            </p>
            <div className="bg-white rounded p-2 font-mono text-xs text-gray-600">
              Actividad,Duración,Predecesoras<br/>
              Excavación,5,<br/>
              Cimentación,10,Excavación
            </div>
          </div>

          {/* Formato 2 */}
          <div>
            <p className="text-sm font-medium text-gray-700 mb-1">
              <span className="bg-green-100 text-green-800 px-2 py-0.5 rounded text-xs mr-2">Formato 2</span>
              Software de gestión
            </p>
            <div className="bg-white rounded p-2 font-mono text-xs text-gray-600">
              Nombre,Duracion,Comienzo,Fin<br/>
              "Torre 01","14 días","13 jul 2026",...
            </div>
          </div>

          <div className="text-xs text-gray-500 pt-2 border-t border-gray-200">
            ℹ️ El sistema detecta automáticamente el formato
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
