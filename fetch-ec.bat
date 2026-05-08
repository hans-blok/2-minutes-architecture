@echo off
REM Fetch ecosysteem-coordinator Script Wrapper
REM 
REM Doel: Roept het Python script aan dat de ecosysteem-coordinator
REM       prompts en agent-contracten ophaalt uit entoli-agents.
REM Usage: fetch-agents.bat [--source path] [--target path] [--dry-run]
REM Example: fetch-agents.bat
REM          fetch-agents.bat --dry-run
REM          fetch-agents.bat --source ..\entoli-agents --target .
REM
REM Vereisten: Python 3.x geïnstalleerd en in PATH

REM Genereer timestamp voor logging (YYYYMMDD-HHMMSS)
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'yyyyMMdd-HHmmss'"') do set timestamp=%%i
set logfile=logs\fetch-agents-%timestamp%.md

echo [INFO] Start fetch ecosysteem-coordinator
echo [INFO] Logging naar: %logfile%
echo.

REM Maak logs directory als die niet bestaat
if not exist logs mkdir logs

REM Roep Python script aan en log output
python scripts\fetch_ecosysteem_coordinator.py %* > "%logfile%" 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Fetch ecosysteem-coordinator gefaald - zie %logfile% voor details
    type "%logfile%"
    exit /b 1
)

echo [OK] Fetch ecosysteem-coordinator succesvol voltooid
echo [INFO] Log beschikbaar in: %logfile%
echo.
type "%logfile%"
