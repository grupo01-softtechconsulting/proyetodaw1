""" URLs for gestion app"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from start.views import RegisterUserAPI, AuthenticateUserAPI, PersonAPI

app_name = 'start'

urlpatterns = [
    path('register-api/', RegisterUserAPI.as_view()),
    path('login-api/', AuthenticateUserAPI.as_view()),
    path('person-api/', PersonAPI.as_view({'get': 'list'})),
    path('person-api/<int:id>/',
         PersonAPI.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
