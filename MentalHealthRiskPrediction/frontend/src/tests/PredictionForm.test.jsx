import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { FEATURE_NAMES, validateVectors } from '../utils/validators.js';
import PredictionForm from '../components/prediction/PredictionForm.jsx';

describe('PredictionForm.test.jsx', () => {
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
