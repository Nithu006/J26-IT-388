import { useEffect, useRef, useState } from 'react';
import PredictionForm from './components/prediction/PredictionForm.jsx';
import PredictionResult from './components/prediction/PredictionResult.jsx';
import { getModelInfo, predict } from './services/predictionService.js';
import './index.css';
export default function App() {
  const [info, setInfo] = useState(null), [connection, setConnection] = useState('Checking API…');
  const [loading, setLoading] = useState(false), [result, setResult] = useState(null), [error, setError] = useState('');
  const refreshSequence = useRef(0);
  async function refresh() {
    const sequence = ++refreshSequence.current;
    setConnection('Checking API…');
    try { const data = await getModelInfo(); if (sequence !== refreshSequence.current) return; setInfo(data); setConnection('API connected'); }
    catch (e) { if (sequence !== refreshSequence.current) return; setInfo(null); setConnection(e.message); }
  }
  useEffect(() => { refresh(); return () => { refreshSequence.current++; }; }, []);
  async function submit(features) {
    setLoading(true); setError(''); setResult(null);
    try { setResult(await predict(features)); }
    catch (e) { setError(e.message); if (e.status === 503) setInfo(old => ({ ...old, available: false })); }
    finally { setLoading(false); }
  }
  return <><header><a className="brand" href="#">M<span> / </span>Research Lab</a><span className="project-id">J26-IT-388 · Research prototype</span></header>
    <main><div className="intro"><div><span className="eyebrow">MULTIMODAL AI / SUPERVISOR DEMONSTRATION</span>
      <h1>Explore the interface.<br/><em>Keep the evidence clear.</em></h1>
      <p>Real-Time Explainable AI-Based Mental Health Risk Prediction Using Social Media</p></div>
      <aside className="status-box"><span className="eyebrow">SERVICE STATUS</span><strong>{info?.available ? 'Model loaded' : 'Model not trained / unavailable'}</strong>
        <span role="status">{connection}</span><button className="secondary" onClick={refresh}>Refresh connection</button></aside></div>
      <section className="notice"><strong>Exploratory research only</strong><p>220 records — below the required 1,000. Label meaning and feature provenance require verification. This interface is not a clinical diagnostic system. No model performance has been established.</p></section>
      <div className="workspace"><PredictionForm onSubmit={submit} loading={loading}/><div><PredictionResult result={result} error={error} loading={loading}/>
        <section className="method"><span className="eyebrow">WHAT THIS DEMONSTRATES</span><h3>A transparent request flow</h3><p>16 numeric inputs → validated API request → model availability check.</p><p>Participant ID, source, risk_oof and label are excluded from inputs. A missing model returns HTTP 503, never a fabricated prediction.</p></section></div></div>
    </main><footer>Multimodal AI Fusion &amp; Risk Prediction <span>Local demonstration · No clinical claims</span></footer></>;
}
