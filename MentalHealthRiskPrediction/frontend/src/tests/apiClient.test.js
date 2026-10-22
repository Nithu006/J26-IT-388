import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { FEATURE_NAMES, validateVectors } from '../utils/validators.js';
import { request } from '../services/apiClient.js';
import { getModelInfo, predict } from '../services/predictionService.js';
afterEach(() => vi.unstubAllGlobals());

describe('apiClient.test.js', () => {
  it('reports network failure and validation errors', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValueOnce(new Error()).mockResolvedValueOnce({ok:false,status:422}));
    await expect(request('/model-info')).rejects.toMatchObject({status:0});
    await expect(request('/predict')).rejects.toMatchObject({status:422});
  });
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
  it('maps other server errors without exposing their contents', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ok:false,status:500}));
    await expect(request('/predict')).rejects.toMatchObject({status:500,message:'The API could not complete the request. Please retry.'});
  });
});

it('accepts the documented unavailable model-info contract', async () => {
  const data = {available:false,features:FEATURE_NAMES,model_version:null,purpose:'exploratory_recorded_label'};
  vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:true,json:async()=>data}));
  await expect(getModelInfo()).resolves.toEqual(data);
});
it('rejects reordered features and a boolean predicted label', async () => {
  const info = {available:false,features:[...FEATURE_NAMES].reverse(),model_version:null,purpose:'exploratory_recorded_label'};
  vi.stubGlobal('fetch',vi.fn().mockResolvedValueOnce({ok:true,json:async()=>info})
    .mockResolvedValueOnce({ok:true,json:async()=>({predicted_label:true,model_version:'fixture',purpose:'exploratory_recorded_label',notice:'fixture'})}));
  await expect(getModelInfo()).rejects.toMatchObject({status:502});
  await expect(predict({})).rejects.toMatchObject({status:502});
});
