import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.error || error.message || 'Error desconocido';
    throw new Error(message);
  }
);

export const processInput = async (input, type = 'text') => {
  const response = await api.post('/api/process', {
    input,
    type
  });
  return response.data;
};

export const optimizeSchedule = async () => {
  const response = await api.post('/api/optimize');
  return response.data;
};

export const sendChatMessage = async (message) => {
  const response = await api.post('/api/chat', {
    question: message
  });
  return response.data;
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getStatus = async () => {
  const response = await api.get('/api/status');
  return response.data;
};

export default api;
