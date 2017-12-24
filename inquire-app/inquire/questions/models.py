from django.db import models

from inquire.profiles.models import UserProfile


class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    object_type = "tag"

    def __str__(self):
        return self.tag


class Question(models.Model):
    question_title = models.CharField(max_length=100)
    question_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    modification_time = models.DateTimeField('date modified')
    author = models.ForeignKey(UserProfile, null=True)
    up_list = models.ManyToManyField(UserProfile, related_name="question_up_list")
    down_list = models.ManyToManyField(UserProfile, related_name="question_down_list")
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    number_of_answers = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)

    object_type = "question"

    def __str__(self):
        return self.question_title


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    modification_time = models.DateTimeField('date modified')
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    net_votes = models.IntegerField(default=0)
    up_list = models.ManyToManyField(UserProfile, related_name="answer_up_list")
    down_list = models.ManyToManyField(UserProfile, related_name="answer_down_list")
    author = models.ForeignKey(UserProfile)

    object_type = "answer"

    def __str__(self):
        return self.answer_text
