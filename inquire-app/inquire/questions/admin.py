from django.contrib import admin

from inquire.questions.models import Answer
from inquire.questions.models import Question
from inquire.questions.models import Tag


admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Tag)
