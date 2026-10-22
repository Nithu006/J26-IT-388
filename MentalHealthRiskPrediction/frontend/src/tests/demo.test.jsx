import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import App from '../App.jsx';
import PredictionForm from '../components/prediction/PredictionForm.jsx';
import PredictionResult from '../components/prediction/PredictionResult.jsx';
import { getModelInfo, predict } from '../services/predictionService.js';
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
    const fetcher = vi.fn().mockResolvedValueOnce({ok:true,json:async()=>({available:false, features:FEATURE_NAMES, model_version:null, purpose:'exploratory_recorded_label'})})
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

describe('API reliability', () => {
  it('converts malformed JSON into a safe message', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ok:true,status:200,json:async()=>{throw new Error('private response');}}));
    await expect(request('/model-info')).rejects.toMatchObject({message:'The API returned an invalid response. Please retry.'});
  });
  it('rejects unexpected successful model-info and prediction payloads', async () => {
    for (const data of [null, [], {}, {available:'yes'}, {predicted_label:true}]) {
      vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ok:true,json:async()=>data}));
      await expect(getModelInfo()).rejects.toMatchObject({status:502});
      await expect(predict({})).rejects.toMatchObject({status:502});
    }
  });
  it('keeps the newest refresh status when an older request fails later', async () => {
    let rejectOld;
    const pending = new Promise((resolve,reject)=>{rejectOld=reject;});
    vi.stubGlobal('fetch', vi.fn().mockReturnValueOnce(pending).mockResolvedValueOnce({ok:true,json:async()=>({available:false,features:FEATURE_NAMES,model_version:null,purpose:'exploratory_recorded_label'})}));
    render(<App/>);
    fireEvent.click(screen.getByRole('button',{name:'Refresh connection'}));
    await screen.findByText('API connected');
    await act(async()=>{rejectOld(new Error('old failure'));});
    expect(screen.getByText('API connected')).toBeInTheDocument();
  });
  it('maps other server errors without exposing their contents', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ok:false,status:500}));
    await expect(request('/predict')).rejects.toMatchObject({status:500,message:'The API could not complete the request. Please retry.'});
  });
});

describe('Accessible vector feedback', () => {
  it('focuses the first invalid field and clears corrected errors', () => {
    const submit = vi.fn(); render(<PredictionForm onSubmit={submit}/>);
    fireEvent.click(screen.getByRole('button',{name:/Request prediction/}));
    const first = document.getElementById('bvec_0');
    expect(first).toHaveFocus();
    expect(screen.getByRole('alert')).toHaveTextContent('16 vector input(s)');
    expect(first).toHaveAttribute('aria-describedby','bvec_0-error');
    fireEvent.change(first,{target:{value:'0'}});
    expect(first).toHaveAttribute('aria-invalid','false');
    expect(first).not.toHaveAttribute('aria-describedby');
    expect(screen.getByRole('alert')).toHaveTextContent('15 vector input(s)');
    fireEvent.click(screen.getByRole('button',{name:/Request prediction/}));
    expect(document.getElementById('bvec_1')).toHaveFocus();
    expect(submit).not.toHaveBeenCalled();
  });
  it('disables form controls while a request is pending', () => {
    render(<PredictionForm loading={true} onSubmit={vi.fn()}/>);
    for (const input of screen.getAllByRole('spinbutton')) expect(input).toBeDisabled();
    expect(screen.getByRole('button',{name:/Requesting/})).toBeDisabled();
  });
});
