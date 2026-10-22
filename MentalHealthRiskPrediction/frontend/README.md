# Frontend

The React application is mounted by `src/main.jsx` and served by Vite. Dependencies
are pinned in `package.json` and `package-lock.json`; `node_modules` and `dist` are
local ignored outputs. The copied checkout's dependencies were installed and its
five active tests and production build passed before this documentation update.

## Working interface

The interface provides 16 numeric vector fields, required/finite-number validation,
loading states, API connection refresh, network/422/503 error messages and a result
section. It clears the previous result before sending another request. It stays
usable when the backend or model is unavailable and does not invent predictions.
The research notice refers to the original 220-record audit, not data shipped here.

The default API URL is `http://127.0.0.1:8000`; configure `VITE_API_BASE_URL` through
the process environment if needed. See the [local demo guide](../docs/local_demo.md)
for startup instructions, dependency prerequisites and endpoint details.

From this `frontend/` directory, with dependencies installed:

```powershell
npm.cmd test
npm.cmd run build
npm.cmd run dev
```

For a fresh checkout, restore dependencies with `npm.cmd ci` after installation is
authorized. Do not assume a clone includes dependencies. The documented verified
local tools are Node.js 22.14.0 and npm 10.9.2.

## Test scope and unfinished features

`vite.config.js` currently selects only `src/tests/demo.test.jsx`, containing five
active tests. Other test files are placeholders outside that selection. The tests
use mocked API responses, not a live backend or research model. A build checks
bundling; it does not validate model performance.

Login, history, dashboard, explanation charts and raw-text workflow components are
placeholders, not working screens. The implemented result renderer can display a
future real API result, but no trained model is supplied. There is no validated
mental-health prediction, probability estimate or clinical diagnosis.
