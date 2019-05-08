""" URLs for gestion app"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from start.views import RegisterUserAPI, AuthenticateUserAPI

app_name = 'start'

urlpatterns = [
    path('register-api/', RegisterUserAPI.as_view()),
    path('login-api/', AuthenticateUserAPI.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
