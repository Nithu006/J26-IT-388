export const FEATURE_NAMES = Array.from({ length: 16 }, (_, i) => `bvec_${i}`);
export function validateVectors(values) {
  const errors = {};
  for (const name of FEATURE_NAMES) {
    if (String(values[name] ?? '').trim() === '' || !Number.isFinite(Number(values[name])))
      errors[name] = 'Enter a finite number.';
  }
  return errors;
}
