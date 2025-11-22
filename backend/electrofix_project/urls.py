
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView, RedirectView
from django.http import JsonResponse, Http404
from django.shortcuts import render
from electrofix_app.mongodb import MongoDBManager
from django.conf import settings
from django.conf.urls.static import static
from pathlib import Path

# Import views
from electrofix_app.views.auth import register, login, profile
from electrofix_app.views.services import get_services, get_service
from electrofix_app.views.bookings import create_booking, get_user_bookings
from electrofix_app.views.orders import create_order, get_user_orders, list_technicians

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'ElectroFix Backend',
        'python_version': '3.14.0'
    })

def test_mongodb(request):
    try:
        db = MongoDBManager.get_db()
        collections = db.list_collection_names()
        return JsonResponse({
            'status': 'ok',
            'database': settings.MONGODB_NAME,
            'collections': collections,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health check
    path('api/health/', health_check, name='health_check'),
    path('api/test/mongodb/', test_mongodb, name='test_mongodb'),
    
    # Authentication
    path('api/auth/register/', register, name='register'),
    path('api/auth/login/', login, name='login'),
    path('api/auth/forgot-password/', __import__('electrofix_app.views.auth', fromlist=['forgot_password']).forgot_password, name='forgot_password'),
    path('api/auth/reset-password/', __import__('electrofix_app.views.auth', fromlist=['reset_password']).reset_password, name='reset_password'),
    path('api/auth/profile/', profile, name='profile'),
    
    # Services
    path('api/services/', get_services, name='get_services'),
    path('api/services/<str:service_id>/', get_service, name='get_service'),
    
    # Bookings
    path('api/bookings/', create_booking, name='create_booking'),
    path('api/bookings/my-bookings/', get_user_bookings, name='get_user_bookings'),
    # Orders / Checkout
    path('api/orders/', create_order, name='create_order'),
    path('api/orders/my-orders/', get_user_orders, name='get_user_orders'),

    # Technicians
    path('api/technicians/', list_technicians, name='list_technicians'),
    
    # Frontend (serve file directly from frontend directory)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    # Redirect legacy /index.html requests to root to prevent duplicate template handling & stale cached 404s
    path('index.html', RedirectView.as_view(pattern_name='home', permanent=False), name='home_index'),
]

# --- Frontend pages and assets in development ---
# Compute frontend dir relative to backend BASE_DIR
FRONTEND_DIR = (Path(settings.BASE_DIR).parent / 'frontend').resolve()

def serve_frontend_page(request, page: str):
    # Only allow templates within the frontend/pages directory
    template_name = f'pages/{page}'
    try:
        return render(request, template_name)
    except Exception:
        # Fall through to 404 if template not found
        raise Http404()

# Serve HTML pages like /pages/login.html, /pages/register.html, etc.
urlpatterns += [
    path('pages/<path:page>', serve_frontend_page, name='frontend_page'),
]

# Serve static assets referenced by the HTML (e.g., /css/custom.css, /js/*.js, /images/*)
if settings.DEBUG and FRONTEND_DIR.exists():
    urlpatterns += static('css/', document_root=str(FRONTEND_DIR / 'css'))
    urlpatterns += static('js/', document_root=str(FRONTEND_DIR / 'js'))
    urlpatterns += static('images/', document_root=str(FRONTEND_DIR / 'images'))
