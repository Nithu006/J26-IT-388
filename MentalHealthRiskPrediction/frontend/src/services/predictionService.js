import { request } from './apiClient.js';
export const getModelInfo = () => request('/model-info');
export const predict = features => request('/predict', { method: 'POST', body: JSON.stringify({ features }) });
