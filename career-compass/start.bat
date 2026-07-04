@echo off
setlocal
cd /d "%~dp0"

echo Starting Career Compass...

start "Career Compass - Backend" cmd /k "cd backend && (if not exist venv python -m venv venv) && call venv\Scripts\activate && pip install -r requirements.txt -q && uvicorn main:app --reload --port 8000"

timeout /t 4 /nobreak >nul

start "Career Compass - Frontend" cmd /k "cd frontend && (if not exist node_modules npm install) && npm run dev"

timeout /t 6 /nobreak >nul

start http://localhost:5173

endlocal