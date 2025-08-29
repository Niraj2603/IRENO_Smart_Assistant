@echo off
echo Starting IRENO Smart Assistant Development Environment...
echo.

REM Start backend Flask server
echo [1/2] Starting Flask backend server...
cd backend
start cmd /k "python app_working.py"
cd ..

REM Start frontend development server
echo [2/2] Starting React frontend server...
cd frontend
start cmd /k "npm run dev"
cd ..

echo.
echo ✅ Development servers are starting...
echo 📱 Frontend will be available at: http://localhost:5173
echo 🔧 Backend will be available at: http://localhost:5000
echo.
echo Press any key to exit...
pause > nul
