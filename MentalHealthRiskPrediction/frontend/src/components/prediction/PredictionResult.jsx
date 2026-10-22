export default function PredictionResult({ result, error, loading }) {
  return <section className="panel result" aria-live="polite" aria-busy={loading}>
    <span className="eyebrow">OUTPUT</span><h2>Recorded-label prediction</h2>
    {loading ? <p role="status">Waiting for the API…</p> : error ? <div role="alert" className="error">{error}</div> :
      result ? <><p className="label-value">Label {result.predicted_label}</p><p>Model version: {result.model_version}</p><p>{result.notice}</p></> :
      <><div className="empty-icon" aria-hidden="true">—</div><p>No prediction yet</p><p className="muted">A result appears only when the API returns a prediction from a loaded model.</p></>}
  </section>;
}
