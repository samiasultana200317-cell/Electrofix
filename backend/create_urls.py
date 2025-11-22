# This script will create the urls.py file
content = '''from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'ElectroFix Backend',
        'python_version': '3.14.0'
    })

def test_mongodb(request):
    try:
        from electrofix_app.mongodb import MongoDBManager
        client = MongoDBManager.get_client()
        db = MongoDBManager.get_db()
        return JsonResponse({
            'status': 'success',
            'message': 'MongoDB connected successfully',
            'database': 'electrofix'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'MongoDB connection failed: {str(e)}'
        }, status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/test/mongodb/', test_mongodb, name='test_mongodb'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('pages/<path:page>', TemplateView.as_view(template_name='index.html'), name='frontend_pages'),
]
'''

with open('electrofix_project/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ urls.py created successfully')
