import os
import sys

# Add the project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Import Django after path is set
from django.core.wsgi import get_wsgi_application

# Initialize Django application (this will load settings)
try:
    application = get_wsgi_application()
except Exception as e:
    # If initialization fails, log the error
    import traceback
    print(f"Django initialization error: {e}")
    print(traceback.format_exc())
    raise

