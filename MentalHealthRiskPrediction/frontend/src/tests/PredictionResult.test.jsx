import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { FEATURE_NAMES, validateVectors } from '../utils/validators.js';
import PredictionResult from '../components/prediction/PredictionResult.jsx';

describe('PredictionResult.test.jsx', () => {
  it('shows loading and clears output while waiting', () => {
    render(<PredictionResult loading={true}/>);
    expect(screen.getByRole('status')).toHaveTextContent('Waiting for the API');
  });
});

it('shows an empty state without a fabricated label', () => {
  render(<PredictionResult/>);
  expect(screen.getByText('No prediction yet')).toBeInTheDocument();
  expect(screen.queryByText(/Label [01]/)).not.toBeInTheDocument();
});
it('suppresses an old result during loading or error', () => {
  const fixture = {predicted_label:0,model_version:'software-test-only',notice:'Mock interface fixture'};
  const {rerender} = render(<PredictionResult result={fixture}/>);
  expect(screen.getByText('Label 0')).toBeInTheDocument();
  rerender(<PredictionResult result={fixture} loading={true}/>);
  expect(screen.queryByText('Label 0')).not.toBeInTheDocument();
  rerender(<PredictionResult result={fixture} error="Model not trained / unavailable"/>);
  expect(screen.getByRole('alert')).toHaveTextContent('Model not trained / unavailable');
  expect(screen.queryByText('Label 0')).not.toBeInTheDocument();
});
