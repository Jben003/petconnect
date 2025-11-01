"""
WSGI configuration for PythonAnywhere deployment
Copy this content to your WSGI configuration file in PythonAnywhere Web tab
"""

import os
import sys

# Add your project directory to the path
# REPLACE 'yourusername' with your actual PythonAnywhere username
path = '/home/yourusername/petconnect'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'petconnect.settings'

# Add virtual environment site-packages to path
venv_python_lib = os.path.join(path, 'venv', 'lib', 'python3.10', 'site-packages')
if os.path.exists(venv_python_lib):
    sys.path.insert(0, venv_python_lib)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

