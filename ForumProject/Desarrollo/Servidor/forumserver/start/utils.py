""" Utils for gestion app """
from django.contrib.auth.models import User

from start.models import Person


def create_user(dict_post):
    """ Function to create an user and person """
    exists_user = User.objects.filter(email=dict_post['email']).exists()
    if not exists_user:
        dict_post['first_name'] = (dict_post['first_name']).title()
        dict_post['last_name'] = (dict_post['last_name']).title()
        username = dict_post['username']
        user = User.objects.create(username=username,
                                   email=dict_post['email'],
                                   password="",
                                   first_name=dict_post['first_name'],
                                   last_name=dict_post['last_name'])
        user.set_password(dict_post['password'])
        user.save()
        person = Person.objects.create(user=user)
        person.save()
        return user
    else:
        return None
