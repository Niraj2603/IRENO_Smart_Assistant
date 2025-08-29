# IRENO Smart Assistant Development Environment Launcher
# PowerShell script to start both frontend and backend servers

Write-Host "Starting IRENO Smart Assistant Development Environment..." -ForegroundColor Green
Write-Host ""

# Function to start backend
function Start-Backend {
    Write-Host "[1/2] Starting Flask backend server..." -ForegroundColor Yellow
    Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd backend; python app_working.py"
}

# Function to start frontend
function Start-Frontend {
    Write-Host "[2/2] Starting React frontend server..." -ForegroundColor Yellow
    Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
}

# Start both services
Start-Backend
Start-Sleep -Seconds 2
Start-Frontend

Write-Host ""
Write-Host "✅ Development servers are starting..." -ForegroundColor Green
Write-Host "📱 Frontend will be available at: http://localhost:5173" -ForegroundColor Cyan
Write-Host "🔧 Backend will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
