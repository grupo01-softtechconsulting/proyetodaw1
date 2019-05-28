""" Views for gestion app """
from rest_framework.viewsets import ModelViewSet

from start.serializers import PersonSerializer
from start.utils import create_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from start.models import Person


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """ Class View used to exempt csrf for a request"""

    def enforce_csrf(self, request):
        """ Overwriting method enforce_csrf """
        return  # To not perform the csrf check previously happening


class AuthenticateUserAPI(APIView):
    """ Api to authenticate an user """
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        """ POST method for authentication """
        if 'username' in self.request.data or 'password' in self.request.data:
            username = request.data['username']
            if username.find('@') != -1:
                email = request.data['username']
                password = request.data['password']
                user = None
                if User.objects.filter(email=email, is_active=True).exists():
                    obj_user = User.objects.filter(email=email,
                                                   is_active=True).last()
                    user = authenticate(username=obj_user.username,
                                        password=password)
                    if user:
                        login(request, user)
                    else:
                        return Response({'status': False})
            else:
                username = request.data['username']
                password = request.data['password']
                user = None
                if User.objects.filter(username=username, is_active=True).exists():
                    obj_user = User.objects.filter(username=username,
                                                   is_active=True).last()
                    user = authenticate(username=obj_user.username,
                                        password=password)
                    if user:
                        login(request, user)
                    else:
                        return Response({'status': False})
            if user:
                # Token Logic here
                person_id = Person.objects.get(user=user).id
                return Response({'status': True, 'person_id': person_id})
        return Response({'status': False})


class PersonAPI(ModelViewSet):
    """ API class to manage Person serializer """
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]
    permission_classes = [AllowAny]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """ Method to redefine the queryset """
        if 'email' in self.request.GET:
            if (Person.objects.filter(user__email=self.request.GET['email'])
                    .exists()):
                queryset = (Person.objects
                            .filter(user__email=self.request.GET['email']))
            else:
                queryset = []
        else:
            queryset = Person.objects.all()
        return queryset



class RegisterUserAPI(APIView):
    """ API used for registration of an user """
    authentication_classes = [CsrfExemptSessionAuthentication,
                              BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        """ POST method to handle the registration """
        dictionary_post = {}
        dictionary_post['first_name'] = self.request.data['first_name']
        dictionary_post['last_name'] = self.request.data['last_name']
        dictionary_post['email'] = self.request.data['email']
        dictionary_post['username'] = self.request.data['username']
        dictionary_post['password'] = self.request.data['password']
        new_user = create_user(dictionary_post)
        if new_user is not None:
            if new_user:
                new_user_auth = authenticate(username=dictionary_post['username'],
                                             password=dictionary_post['password'])
                if new_user_auth:
                    login(request, new_user_auth)
                    return Response({'status': True,
                                     'person_id': new_user.person.id})
                else:
                    return Response({'status': False})
        return Response({'status': False})
