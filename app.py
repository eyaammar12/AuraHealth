import os
import sys

# Add the backend directory to the Python path so 'core' can be found
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Import the Django WSGI application
from core.wsgi import application as app

# This 'app' variable is what gunicorn app:app will look for
