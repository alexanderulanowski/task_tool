from django.http import HttpResponse

from .models import Question


def index(request):
    Question.objects.all().delete()
    Question(question_number='1a', question_text='test question').save()
    Question(question_number='1b', question_text='test question 2').save()
    Question(question_number='1c', question_text='test question 3').save()

    return HttpResponse("Success")