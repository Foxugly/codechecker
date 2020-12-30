"""codecheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from users.views import UserLoginView

@login_required
def home(request):
    c = {}
    return render(request, "index.html", c)


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('answer/', include('answer.urls', namespace='answer')),
    path('question/', include('question.urls', namespace='question')),
    path('chapter/', include('chapter.urls', namespace='chapter')),
    path('course/', include('course.urls', namespace='course')),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
