@echo off
set PYTHONPATH=auth_service
venv\Scripts\python -m pytest tests/unit
pause
