"""Standalone WSGI server for ElectroFix to diagnose runserver termination issues."""
import os
from wsgiref.simple_server import make_server

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrofix_project.settings')

from django.core.wsgi import get_wsgi_application  # noqa

app = get_wsgi_application()

HOST = '127.0.0.1'
PORT = 8050

print(f"Starting wsgiref server on http://{HOST}:{PORT}")
print("Ctrl+C to stop")
httpd = make_server(HOST, PORT, app)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Server stopped")
