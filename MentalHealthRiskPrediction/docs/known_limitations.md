# Known limitations

- Dataset, labels, languages, feature windows and supervisor approval are missing.
- Only the PDF, not its original TAF, was supplied.
- The loader supports in-memory CSV only; large/Parquet data will require adaptation.
- Audit checks exact rows and whitespace-normalized text, not semantic near duplicates.
- It reports repeated groups but does not create splits or certify absence of leakage.
- Language and permissions require human evidence; neither is inferred or verified.
- No clinical validity, model quality, calibration or real-time performance is established.
- Training, model serialization, API, React and their tests are not implemented yet.
- The audit has no third-party dependencies; future ML/application pins remain pending.
