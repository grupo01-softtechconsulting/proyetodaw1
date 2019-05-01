""" Admin for gestion app """
from django.contrib import admin
from start.models import Person, PersonImage, Role

admin.site.register(Person)
admin.site.register(PersonImage)
admin.site.register(Role)
