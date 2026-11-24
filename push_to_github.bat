@echo off
title Push Patient Health Monitoring System to GitHub
color 0b

echo ================================================================
echo    PATIENT HEALTH MONITORING SYSTEM — GITHUB PUSH WIZARD
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Git installation...
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)
echo [OK] Git is installed.
echo.

echo [2/4] Initializing / updating repository...
if not exist ".git" (
    git init -b main
) else (
    git branch -M main
)

git add -A
git commit -m "Initial commit: Patient Health Monitoring System with IoT Blynk, Live Web Dashboard, and Simulation" >nul 2>&1
echo [OK] All project files committed.
echo.

echo [3/4] GitHub Repository Configuration
echo ----------------------------------------------------------------
echo If you have not created a GitHub repository yet:
echo   1. Open https://github.com/new in your browser
echo   2. Repository Name : Patient_Health_Monitoring_System
echo   3. Set to Public (recommended for college projects)
echo   4. Do NOT initialize with README/license (we already have them)
echo   5. Click 'Create repository' and copy the HTTPS URL
echo ----------------------------------------------------------------
echo.

set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/username/Patient_Health_Monitoring_System.git): "

if "%REPO_URL%"=="" (
    echo [WARNING] No repository URL entered.
    echo You can push manually anytime using:
    echo   git remote add origin YOUR_REPO_URL
    echo   git push -u origin main
    echo.
    pause
    exit /b 0
)

echo.
echo [4/4] Setting remote and pushing to GitHub...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git branch -M main

echo Pushing main branch to %REPO_URL%...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo [SUCCESS] Code successfully pushed to GitHub!
    echo.
    echo Live Web Dashboard Setup (Optional free live hosting):
    echo   1. In your GitHub repo, click 'Settings' -> 'Pages'
    echo   2. Under 'Branch', select 'main' and '/ (root)'
    echo   3. Click 'Save'
    echo   Your dashboard will be live at:
    echo   https://your-username.github.io/Patient_Health_Monitoring_System/
    echo ================================================================
) else (
    echo.
    echo [NOTE] If GitHub asked for a password, note that GitHub requires a
    echo Personal Access Token (PAT) instead of your account password.
    echo Create one at: https://github.com/settings/tokens (classic token with 'repo' scope)
)

echo.
pause
