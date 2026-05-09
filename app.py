import os
import sys

# Get the absolute path of the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(base_dir, 'backend')

# Add it to sys.path if it exists (for root-level execution)
if os.path.exists(backend_path):
    sys.path.insert(0, backend_path)

# Import the Django WSGI application
try:
    from core.wsgi import application as app
except ImportError:
    # Fallback for different directory structures
    from core.wsgi import application as app
