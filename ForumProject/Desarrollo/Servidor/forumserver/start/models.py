""" Models for start app """
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Role(models.Model):
    """
    Class of available roles for a person
    Values:
    - 1: professor
    - 2: student
    """
    PROFESSOR = 'professor'
    STUDENT = 'student'
    ROLE_TYPES = (
        (1, PROFESSOR),
        (2, STUDENT)
    )
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    value = models.IntegerField(choices=ROLE_TYPES, default=3)

    def __str__(self):
        return str(self.value) + ' ' + self.name


class Person(models.Model):
    """
    Model for extra data for a user
    Values for typ
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    born_date = models.DateField(blank=True, null=True)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.get_full_name()


class PersonImage(models.Model):
    """ Images in general for the project """
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/users/profile',
                              blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.person.user.get_full_name() + ': ' + self.image.url
