import { request, ApiError } from './apiClient.js';
import { FEATURE_NAMES } from '../utils/validators.js';
const PURPOSE = 'exploratory_recorded_label';
const invalid = () => new ApiError('The API returned an unexpected response. Please retry.', 502);
const version = value => typeof value === 'string' && value.trim().length > 0;
export async function getModelInfo() {
  const data = await request('/model-info');
  if (!data || typeof data.available !== 'boolean' || data.purpose !== PURPOSE ||
      !Array.isArray(data.features) || data.features.length !== FEATURE_NAMES.length ||
      !data.features.every((name, i) => name === FEATURE_NAMES[i]) ||
      (data.available ? !version(data.model_version) : data.model_version !== null)) throw invalid();
  return data;
}
export async function predict(features) {
  const data = await request('/predict', { method: 'POST', body: JSON.stringify({ features }) });
  if (!data || ![0, 1].includes(data.predicted_label) || !version(data.model_version) ||
      data.purpose !== PURPOSE || typeof data.notice !== 'string' || !data.notice.trim()) throw invalid();
  return data;
}
