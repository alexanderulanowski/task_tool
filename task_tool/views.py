import random

from django.http import HttpResponse
from django.template import loader

from .models import Answer
from .models import Question


def index(request):
    # latest_question_list = Question.objects.order_by('-question_number')[:5]
    username = ''.join([random.choice('abcdefgijklmnopqrstuvw0123456789') for _ in range(6)])
    template = loader.get_template('index.html')
    context = {
        'username': username,
    }
    return HttpResponse(template.render(context, request))


def all(request, username):
    template = loader.get_template('all.html')

    qs = Question.objects.order_by('-question_number').reverse()
    context = {
        'question_list': qs
    }

    return HttpResponse(template.render(context, request))

def questions(request, username, question_id=''):
    template = loader.get_template('questions.html')

    if request.method == 'POST':
        q = Question.objects.get(question_number=request.POST.get("question_number"))
        Answer(question=q, user=username, answer_text=request.POST.get("answer")).save()

    qs = Question.objects.order_by('-question_number').reverse()
    print [q.question_number for q in qs]

    qn = None
    qp = None
    q = None

    qi = -1
    if len(question_id) != 0:
        for i in range(len(qs)):
            if qs[i].question_number == question_id:
                qi = i
    else:
        qi = 0

    if qi < len(qs) and qi >= 0:
        q = qs[qi]
        if qi + 1 < len(qs):
            qn = qs[qi + 1]

        if qi - 1 >= 0:
            qp = qs[qi - 1]

    if q == None:
        return HttpResponse("Question not found")

    answer_text = ''
    answer = Answer.objects.filter(user=username, question=q)
    if len(answer) > 0:
        print "found answer"
        answer_text = answer.last().answer_text

    context = {
        'question_list': qs,
        'question': q,
        'qn': qn,
        'qp': qp,
        'answer': answer_text
    }

    return HttpResponse(template.render(context, request))


def answers(request, question_id = ''):
    template = loader.get_template('answers.html')

    qs = Question.objects.order_by('-question_number').reverse()

    answers = []
    if len(question_id) > 0:
        q = Question.objects.get(question_number = question_id)
        all_answers = Answer.objects.filter(question=q)
        users = set([a.user for a in all_answers])

        for user in users:
            answers_by_user = Answer.objects.filter(user=user, question=q)
            answers.append(answers_by_user.last())

    context = {
        'question_list': qs,
        'answers': answers
    }

    return HttpResponse(template.render(context, request))
