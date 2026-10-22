import { useState } from 'react';
import { FEATURE_NAMES, validateVectors } from '../../utils/validators.js';
export default function PredictionForm({ onSubmit, loading }) {
  const [values, setValues] = useState(Object.fromEntries(FEATURE_NAMES.map(k => [k, ''])));
  const [errors, setErrors] = useState({});
  function submit(event) {
    event.preventDefault();
    const next = validateVectors(values); setErrors(next);
    const invalid = Object.keys(next);
    if (invalid.length) event.currentTarget.querySelector(`#${invalid[0]}`)?.focus();
    if (!invalid.length) onSubmit(Object.fromEntries(FEATURE_NAMES.map(k => [k, Number(values[k])])));
  }
  function change(name, value) {
    const updated = { ...values, [name]: value };
    setValues(updated);
    if (!validateVectors(updated)[name]) setErrors(current => {
      const next = { ...current }; delete next[name]; return next;
    });
  }
  return <form className="panel" onSubmit={submit} noValidate>
    <span className="eyebrow">INPUT / 16 DIMENSIONS</span><h2>Behavior-vector inputs</h2>
    <p className="muted">Enter an authorized vector. Feature meanings and valid research ranges are not yet verified.</p>
    {Object.keys(errors).length > 0 && <div role="alert" className="field-error">
      Please correct {Object.keys(errors).length} vector input(s). Focus is on the first invalid field after submission.
    </div>}
    <fieldset disabled={loading}><legend className="sr-only">Vector values</legend><div className="vector-grid">
      {FEATURE_NAMES.map((name, i) => <div key={name}><label htmlFor={name}>{name}<span>{String(i + 1).padStart(2, '0')}</span></label>
        <input id={name} type="number" step="any" value={values[name]} aria-invalid={Boolean(errors[name])}
          aria-describedby={errors[name] ? `${name}-error` : undefined}
          onChange={e => change(name, e.target.value)} placeholder="Numeric value" />
        {errors[name] && <small className="field-error" id={`${name}-error`}>{errors[name]}</small>}</div>)}
    </div></fieldset>
    <div className="form-actions"><button type="submit" disabled={loading}>{loading ? 'Requesting…' : 'Request prediction →'}</button><span>No input history is stored.</span></div>
  </form>;
}
