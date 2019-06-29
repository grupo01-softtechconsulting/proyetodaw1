""" Views for the question app """
from django.db.models import Count
from django.db.models import Q
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from question.models import (
    Question, QuestionImage, Answer)
from question.serializers import (
    QuestionSerializer, QuestionImageSerializer,
    AnswerSerializer)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """ Class View used to exempt csrf for a request"""

    def enforce_csrf(self, request):
        """ Overwriting method enforce_csrf """
        return  # To not perform the csrf check previously happening


class QuestionAPI(ModelViewSet):
    """ API view to manage reports """
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """ Redefinition of queryset for the view """
        if 'person_id' in self.request.GET:
            '''if 'by_tag' in self.request.GET:
                queryset = (Question.objects.all()
                            .order_by('-questiontag__tag__name'))
            elif 'newest' in self.request.GET:
                queryset = (Question.objects.all()
                            .order_by('-creation_date'))
            elif 'oldest' in self.request.GET:
                queryset = (Question.objects.all()
                            .order_by('creation_date'))
            elif 'by_likes' in self.request.GET:
                only_likes = Count('questionpersonlike',
                                    filter=Q(questionpersonlike__like=True))
                queryset = (Question.objects.annotate(only_likes=only_likes)
                            .order_by('-only_likes'))
            elif 'id_tag' in self.request.GET:
                queryset = (Question.objects
                            .filter(questiontag__tag__id=self.request
                                    .GET['id_tag']))'''
            queryset = (Question.objects
                        .filter(creator__id=self.request.GET['person_id']))
        else:
            queryset = Question.objects.all()
        if 'autor_text' in self.request.GET:
            text_search = self.request.GET['autor_text']
            queryset = (queryset.filter(Q(creator__user__first_name__icontains=text_search) |
                                        Q(creator__user__last_name__icontains=text_search)))
        if 'last_questions' in self.request.GET:
            queryset = (queryset.order_by('-creation_date')[:5])
        else:
            if 'by_tag' in self.request.GET:
                queryset = (queryset.order_by('-questiontag__tag__name'))
            elif 'newest' in self.request.GET:
                queryset = (queryset.order_by('-creation_date'))
            elif 'oldest' in self.request.GET:
                queryset = (queryset.order_by('creation_date'))
        return queryset


class QuestionImageAPI(ModelViewSet):
    """ API view to manage images for person """
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = QuestionImageSerializer
    queryset = QuestionImage.objects.all()
    lookup_field = 'question__id'


class AnswerAPI(ModelViewSet):
    """ API view to manage answers for a question """
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = AnswerSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """ Redefinition of queryset for the view """
        if 'person_id' in self.request.GET:
            queryset = (Answer.objects
                        .filter(creator__id=self.request.GET['person_id']))
        elif 'question_id' in self.request.GET:
            queryset = (Answer.objects.filter(question__id=self.request
                                              .GET['question_id']))
        else:
            queryset = Answer.objects.all()
        return queryset

