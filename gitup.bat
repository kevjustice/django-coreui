@echo off
setlocal EnableDelayedExpansion

IF "%~1"=="" (
    echo Error: Please provide a commit message
    echo Usage: gitpush "Your commit message"
    pause
    exit /b 1
)

echo Pulling latest changes...
git pull origin main
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Pull failed
    pause
    exit /b 1
)

echo Adding all changes...
git add -A
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Add failed
    pause
    exit /b 1
)

echo Committing changes...
git commit -m "%~1"
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Commit failed
    pause
    exit /b 1
)

echo Pushing to repository...
git push origin main
IF %ERRORLEVEL% NEQ 0 (
    echo Error: Push failed
    pause
    exit /b 1
)

echo.
echo Successfully completed all git operations
echo.
pause
