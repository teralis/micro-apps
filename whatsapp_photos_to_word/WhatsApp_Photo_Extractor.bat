@echo off
title WhatsApp Photo Extractor
echo.
echo Starting WhatsApp Photo Extractor...
echo.

REM Change to src directory and check if Python script exists
cd /d "%~dp0\src"
if not exist "whatsapp_photo_extractor.py" (
    echo Error: whatsapp_photo_extractor.py not found in src folder!
    echo Please make sure the Python script is in the src directory.
    pause
    exit /b 1
)

REM Run the Python script in interactive mode
python whatsapp_photo_extractor.py --interactive

echo.
echo Process completed!
echo Press any key to close this window...
pause >nul