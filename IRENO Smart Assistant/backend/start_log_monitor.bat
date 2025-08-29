@echo off
echo ================================================
echo   IRENO Smart Assistant - Log Monitor
echo ================================================
echo.
echo Choose an option:
echo.
echo 1. Real-time log monitoring
echo 2. Show last 50 log entries
echo 3. Show last 100 log entries
echo 4. Help
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting real-time log monitoring...
    echo Press Ctrl+C to stop monitoring
    echo.
    python monitor_logs.py
) else if "%choice%"=="2" (
    echo Showing last 50 log entries...
    echo.
    python monitor_logs.py recent 50
) else if "%choice%"=="3" (
    echo Showing last 100 log entries...
    echo.
    python monitor_logs.py recent 100
) else if "%choice%"=="4" (
    python monitor_logs.py help
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause
