# frontend

**Update 2026-10-22:** the React/Vite UI is runnable; dependencies are pinned and the
lockfile is saved. Run `npm.cmd run dev`, `npm.cmd test`, or `npm.cmd run build`.
See [local demo guide](../docs/local_demo.md). Earlier scaffold-only statements below
are historical and superseded by this update.

Purpose: reserved location for frontend.
Status: starter structure only; implementation and contracts await review.
No real data, trained model, results, authentication or persistence is provided.
Research use only; not a clinical diagnostic system.

This is a React + Vite source skeleton, not a runnable frontend. `App.jsx` contains
a research notice; `main.jsx` deliberately does not mount it. Other components
are named placeholders returning null. No API requests or fake charts/results occur.

`package.json` is valid ES-module metadata with empty dependency maps. Runtime
dependencies and dev/build/test scripts will be pinned and added after review.
Do not interpret `npm install` as a working setup. No lockfile is generated yet.
The optional `npm run check:scaffold` only syntax-checks one JS service stub.
Full structure checks run from the root: `python scripts/validate_scaffold.py`.
