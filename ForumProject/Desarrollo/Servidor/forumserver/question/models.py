""" Models for question app """
from django.utils import timezone
from django.db import models
from start.models import Person


class Question(models.Model):
    """ Question made by one person """
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=True)
    statement = models.TextField()
    points = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.title:
            title = self.title
        else:
            title = "Sin titulo"
        return (self.creator.user.get_full_name() + ' - ' +
                title + ' - ' + self.statement)


class QuestionImage(models.Model):
    """ Images for questions """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/users/question',
                              blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question.__str__() + ': ' + self.image.url


class QuestionPersonLike(models.Model):
    """ Model to manage likes from persons to an specific question """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (self.question.__str__() + ': ' +
                self.person.user.get_full_name() + ' - Like')


class Answer(models.Model):
    """ Answer made by one user for a question """
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    statement = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    edit_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.creator.user.get_full_name() + ' - ' + self.statement


class Tag(models.Model):
    """ Tag related to a subject """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class QuestionTag(models.Model):
    """ Intermediate table between a question and a tag """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.__str__() + ' - ' + self.tag.name
