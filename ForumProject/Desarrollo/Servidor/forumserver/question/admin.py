from django.contrib import admin
from question.models import (
    Question, QuestionImage, Answer,
    Tag, QuestionTag, QuestionPersonLike)

admin.site.register(Question)
admin.site.register(QuestionImage)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(QuestionTag)
admin.site.register(QuestionPersonLike)
