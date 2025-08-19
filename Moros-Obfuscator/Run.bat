@echo off

where python >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: Python not found in PATH.
    pause
    exit /b
)

net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as admin. Starting moros.py...
    python "%~dp0moros.py"
    goto :keep_open
) else (
    echo Requesting admin access for moros.py...
    powershell -Command "Start-Process python -ArgumentList '\"%~dp0moros.py\"' -Verb RunAs"
    exit
)

:keep_open
pause