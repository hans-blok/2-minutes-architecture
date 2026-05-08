@echo off
REM Commit and Push Script
REM 
REM Doel: Git add, commit met message, en push naar remote
REM Usage: push.bat "commit message"
REM
REM Vereisten: Git geïnstalleerd en in PATH

IF "%~1"=="" (
    echo [ERROR] Commit message is verplicht
    echo Usage: push.bat "commit message"
    exit /b 1
)

echo [INFO] Git add...
git add .
IF ERRORLEVEL 1 (
    echo [ERROR] Git add gefaald
    exit /b 1
)

echo [INFO] Git commit...
git commit -m "%~1"
IF ERRORLEVEL 1 (
    echo [ERROR] Git commit gefaald
    exit /b 1
)

echo [INFO] Git push...
git push
IF ERRORLEVEL 1 (
    echo [ERROR] Git push gefaald
    exit /b 1
)

echo [OK] Changes gepushed naar remote: "%~1"
