const BASE = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
export class ApiError extends Error {
  constructor(message, status) { super(message); this.status = status; }
}
export async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${BASE}${path}`, { ...options, signal: AbortSignal.timeout(10000),
      headers: { 'Content-Type': 'application/json', ...options.headers } });
  } catch { throw new ApiError('Cannot reach the API. Check that the backend is running and retry.', 0); }
  if (!response.ok) {
    if (response.status === 503) throw new ApiError('Model not trained / unavailable', 503);
    if (response.status === 422) throw new ApiError('The API rejected these vector inputs. Check all 16 values.', 422);
    throw new ApiError('The API could not complete the request. Please retry.', response.status);
  }
  try { return await response.json(); }
  catch { throw new ApiError('The API returned an invalid response. Please retry.', response.status); }
}
