import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App.jsx';
import PredictionForm from '../components/prediction/PredictionForm.jsx';
import PredictionResult from '../components/prediction/PredictionResult.jsx';
import { request } from '../services/apiClient.js';
import { FEATURE_NAMES, validateVectors } from '../utils/validators.js';
afterEach(() => vi.unstubAllGlobals());
describe('Research demo', () => {
  it('shows missing-field errors without sending a request', () => {
    const submit = vi.fn(); render(<PredictionForm onSubmit={submit} loading={false}/>);
    fireEvent.click(screen.getByRole('button', {name: /Request prediction/}));
    expect(screen.getAllByText('Enter a finite number.')).toHaveLength(16);
    expect(submit).not.toHaveBeenCalled();
  });
  it('validates finite numbers and orders exactly 16 features', () => {
    const submit = vi.fn(); render(<PredictionForm onSubmit={submit}/>);
    FEATURE_NAMES.forEach(k => fireEvent.change(document.getElementById(k), {target: {value: '0'}}));
    fireEvent.click(screen.getByRole('button', {name: /Request prediction/}));
    expect(Object.keys(submit.mock.calls[0][0])).toEqual(FEATURE_NAMES);
    expect(validateVectors({ ...Object.fromEntries(FEATURE_NAMES.map(k=>[k, 0])), bvec_0: Infinity })).toHaveProperty('bvec_0');
  });
  it('renders interface and handles actual API-shaped 503', async () => {
    const fetcher = vi.fn().mockResolvedValueOnce({ok:true,json:async()=>({available:false})})
      .mockResolvedValueOnce({ok:false,status:503});
    vi.stubGlobal('fetch', fetcher); render(<App/>);
    await screen.findByText('API connected');
    FEATURE_NAMES.forEach(k => fireEvent.change(document.getElementById(k), {target: {value: '0'}}));
    fireEvent.click(screen.getByRole('button', {name:/Request prediction/}));
    await waitFor(()=>expect(screen.getByRole('alert')).toHaveTextContent('Model not trained / unavailable'));
    expect(JSON.parse(fetcher.mock.calls[1][1].body).features).not.toHaveProperty('risk_oof');
    expect(screen.queryByText('Label 1')).not.toBeInTheDocument();
  });
  it('shows loading and clears output while waiting', () => {
    render(<PredictionResult loading={true}/>);
    expect(screen.getByRole('status')).toHaveTextContent('Waiting for the API');
  });
  it('reports network failure and validation errors', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValueOnce(new Error()).mockResolvedValueOnce({ok:false,status:422}));
    await expect(request('/model-info')).rejects.toMatchObject({status:0});
    await expect(request('/predict')).rejects.toMatchObject({status:422});
  });
});
