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
            queryset = Question.objects.all()
            if 'my_questions' in self.request.GET:
                queryset = (queryset.filter(creator__id=self.request.GET['person_id']))
            if 'search_autor' in self.request.GET:
                text_search = self.request.GET['search_autor']
                queryset = (queryset.filter(Q(creator__user__first_name__icontains=text_search) |
                                            Q(creator__user__last_name__icontains=text_search)))
            if 'last_questions' in self.request.GET:
                queryset = (queryset.order_by('-creation_date')[:5])
            else:
                if 'by_tag' in self.request.GET:
                    queryset = (queryset.order_by('-questiontag__tag__name'))
                if 'order_by' in self.request.GET:
                    if self.request.GET['order_by'] == 'newest':
                        queryset = (queryset.order_by('-creation_date'))
                    elif self.request.GET['order_by'] == 'oldest':
                        queryset = (queryset.order_by('creation_date'))
        else:
            queryset = []
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

