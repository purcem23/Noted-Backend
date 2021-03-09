#NotedBackend.wsgi
import sys
sys.path.insert(0, '/var/www/html/NotedBackend')

from src/main import app as application