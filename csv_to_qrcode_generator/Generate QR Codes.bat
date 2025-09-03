@echo off
REM QR Code Generator - Windows Batch File
REM Double-click this file to generate QR codes from input.csv

echo ===================================
echo     QR Code Generator
echo ===================================
echo.

REM Check if input.csv exists
if not exist "input.csv" (
    echo ERROR: input.csv not found!
    echo.
    echo Please create an input.csv file with this format:
    echo filename,url
    echo bou001,http://qrtub.com/_a9f2k
    echo bou002,http://qrtub.com/_z3x7m
    echo.
    pause
    exit /b 1
)

echo Found input.csv file
echo Running QR code generator...
echo.

REM Run the Python script
python qr_generator.py

REM Check if the script ran successfully
if %ERRORLEVEL% == 0 (
    echo.
    echo ===================================
    echo QR codes generated successfully!
    echo Check the timestamped folder for:
    echo - Individual SVG files
    echo - Index PDF with all codes
    echo ===================================
) else (
    echo.
    echo ERROR: Failed to generate QR codes
    echo Make sure Python and required packages are installed:
    echo pip install -r requirements.txt
)

echo.
pause