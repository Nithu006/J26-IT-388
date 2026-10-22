import { useState } from 'react';
import { FEATURE_NAMES, validateVectors } from '../../utils/validators.js';
export default function PredictionForm({ onSubmit, loading }) {
  const [values, setValues] = useState(Object.fromEntries(FEATURE_NAMES.map(k => [k, ''])));
  const [errors, setErrors] = useState({});
  function submit(event) {
    event.preventDefault();
    const next = validateVectors(values); setErrors(next);
    if (!Object.keys(next).length) onSubmit(Object.fromEntries(FEATURE_NAMES.map(k => [k, Number(values[k])])));
  }
  return <form className="panel" onSubmit={submit} noValidate>
    <span className="eyebrow">INPUT / 16 DIMENSIONS</span><h2>Behavior-vector inputs</h2>
    <p className="muted">Enter an authorized vector. Feature meanings and valid research ranges are not yet verified.</p>
    <fieldset disabled={loading}><legend className="sr-only">Vector values</legend><div className="vector-grid">
      {FEATURE_NAMES.map((name, i) => <div key={name}><label htmlFor={name}>{name}<span>{String(i + 1).padStart(2, '0')}</span></label>
        <input id={name} type="number" step="any" value={values[name]} aria-invalid={Boolean(errors[name])}
          aria-describedby={errors[name] ? `${name}-error` : undefined}
          onChange={e => setValues({ ...values, [name]: e.target.value })} placeholder="Numeric value" />
        {errors[name] && <small className="field-error" id={`${name}-error`}>{errors[name]}</small>}</div>)}
    </div></fieldset>
    <div className="form-actions"><button type="submit" disabled={loading}>{loading ? 'Requesting…' : 'Request prediction →'}</button><span>No input history is stored.</span></div>
  </form>;
}
