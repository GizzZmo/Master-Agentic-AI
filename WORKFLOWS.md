# Workflow System

The repository now includes a GitHub Actions CI workflow that validates both the backend and frontend on every push to `main` and on all pull requests.

## Jobs and commands

- **Backend validation**
  - Environment: Python 3.11
  - Steps: `pip install -r backend/requirements.txt`, `python -m compileall backend/app`
  - Purpose: Fail fast on syntax issues without requiring a Gemini API key.

- **Frontend lint and build**
  - Environment: Node.js 20.x
  - Steps: `npm install`, `npm run lint`, `npm run build`
  - Purpose: Enforce linting and ensure the production bundle builds cleanly.

## Run the same checks locally

From the repository root:

```bash
# Backend
python -m compileall backend/app

# Frontend
cd frontend
npm install
npm run lint
npm run build
```

These commands match the CI workflow so contributors can catch issues before opening a pull request.
