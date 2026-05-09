import os
import sys

# Ensure the current directory (backend) is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.wsgi import application as app
