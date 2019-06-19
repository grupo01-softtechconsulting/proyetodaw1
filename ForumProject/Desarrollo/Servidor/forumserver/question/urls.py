""" URLs for question app"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from question.views import (
    QuestionAPI, QuestionImageAPI, AnswerAPI)


app_name = 'question'

urlpatterns = [
    url(r'^question-api/$', QuestionAPI.as_view({'get': 'list',
                                                 'post': 'create'})),
    url(r'^question-api/(?P<id>[0-9]+)/$',
        QuestionAPI.as_view({'get': 'retrieve', 'patch': 'partial_update',
                             'delete': 'destroy'})),
    url(r'^question-image-api/$',
        QuestionImageAPI.as_view({'post': 'create'})),
    url(r'^question-image-api/(?P<question__id>[0-9]+)/$',
        QuestionImageAPI.as_view({'get': 'retrieve',
                                  'patch': 'partial_update'})),
    url(r'^answer-api/$', AnswerAPI.as_view({'get': 'list',
                                             'post': 'create'})),
    url(r'^answer-api/(?P<id>[0-9]+)/$',
        AnswerAPI.as_view({'get': 'retrieve', 'patch': 'partial_update',
                           'delete': 'destroy'}))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
