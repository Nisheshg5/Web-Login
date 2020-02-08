START /high /min pythonw "Kill.py" 1> "KillLogs.log" 2>&1
REM START /min "PythonKillCmd" pythonw "%~dp0Kill.py"