import os
import sys

# Add the project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Import Django after path is set
import django
from django.core.wsgi import get_wsgi_application

# Initialize Django
django.setup()

# Get WSGI application
application = get_wsgi_application()

# CRITICAL: Vercel needs 'app', not 'application'
app = application