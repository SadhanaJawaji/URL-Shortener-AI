@echo off
title URL Shortener App
cd /d "%~dp0"
echo Starting URL Shortener...
echo App will open at http://localhost:8000
start http://localhost:8000
uvicorn main:app --reload
pause