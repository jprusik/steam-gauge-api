import sys, os

PYTHON_DIRECTORY = ''
APP_DIRECTORY = ''

# dotenv is not available until the venv Python (with installed packages) replaces the running Python process (via `os.execl` below)
try:
    with open('.env') as f:
        for line in f:
            if line.startswith('PYTHON_DIRECTORY'):
                PYTHON_DIRECTORY = line.strip().split('=', 1)[1]
            elif line.startswith('APP_DIRECTORY'):
                APP_DIRECTORY = line.strip().split('=', 1)[1]
            else:
                continue
except:
    pass

INTERP = os.path.expanduser(PYTHON_DIRECTORY)

# INTERP is present twice so that the new Python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.insert(0, cwd + APP_DIRECTORY)  # You must add your project here

from app import flaskApp as application
