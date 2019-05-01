""" URLs for gestion app"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from start.views import RegisterUserAPI, AuthenticateUserAPI

app_name = 'start'

urlpatterns = [
    url('register-api/', RegisterUserAPI.as_view()),
    url('login-api/', AuthenticateUserAPI.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
