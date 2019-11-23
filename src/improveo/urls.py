"""improveo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('profiles.urls', namespace='profiles')),
    path('', include('reports.urls', namespace='reports')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)


'''
urls.py (main):
www.example.com/path1/ - view
http://127.0.0.1:8000/test/


urls.py (app):
www.example.com/path1/ - view 1
http://127.0.0.1:8000/test/ 
www.example.com/path1/option1 - view 2
http://127.0.0.1:8000/test/sleep
www.example.com/path1/option2 - view 3
...

'''
