import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { FEATURE_NAMES, validateVectors } from '../utils/validators.js';
import App from '../App.jsx';
afterEach(() => vi.unstubAllGlobals());

describe('demo.test.jsx', () => {
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
});
