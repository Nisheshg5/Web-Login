START /low /min pythonw "Web Login.py" 1> "ErrorLogs.log" 2>&1
REM START /min "PythonCmd" pythonw "%~dp0Web Login.py" 1> "%~dp0ErrorLogs.log" 2>&1