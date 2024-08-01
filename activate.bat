@echo off
REM Change directory to the location of your virtual environment
cd venv\Scripts

REM Activate the virtual environment
call activate

REM Change directory back to the root of your project if necessary
cd ../../

REM open vs code
code .
