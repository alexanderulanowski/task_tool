from django.db import models


class Question(models.Model):
    question_number = models.CharField(max_length=100, unique=True)
    question_text = models.CharField(max_length=10000)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    answer_text = models.CharField(max_length=10000)