import random

from django.http import HttpResponse
from django.template import loader

from .models import Answer
from .models import CurrentGroup
from .models import Group
from .models import Question


class Result:
    def __init__(self, q, done):
        self.q = q
        self.done = done


def get_current_group():
    cg = CurrentGroup.objects.all()
    if len(cg) == 0:
        cg = CurrentGroup(group=Group.objects.all().first())
        cg.save()
    else:
        cg = cg.last()
    return cg.group


def set_current_group(g):
    cg = CurrentGroup.objects.all()
    if len(cg) == 0:
        cg = CurrentGroup(group=Group.objects.all().first())
        cg.save()
    else:
        cg = cg.last()

    cg.group = g
    cg.save()


def index(request):
    # latest_question_list = Question.objects.order_by('-question_number')[:5]
    username = ''.join([random.choice('abcdefgijklmnopqrstuvwxyz0123456789') for _ in range(6)])
    template = loader.get_template('index.html')
    context = {
        'username': username,
    }
    return HttpResponse(template.render(context, request))


def all(request, username):
    template = loader.get_template('all.html')

    qs = Question.objects.order_by('-question_number').reverse()

    def check_for_answers(answers):
        return len(answers) > 0 and len(answers.last().answer_text) > 0

    qs = [Result(q, check_for_answers(Answer.objects.filter(user=username, question=q, group=get_current_group()))) for
          q in qs]
    context = {
        'result_list': qs
    }

    return HttpResponse(template.render(context, request))


def questions(request, username, question_id=''):
    template = loader.get_template('questions.html')

    if request.method == 'POST':
        q = Question.objects.get(question_number=request.POST.get("question_number"))
        Answer(question=q, user=username, group=get_current_group(), answer_text=request.POST.get("answer")).save()

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
    answer = Answer.objects.filter(user=username, question=q, group=get_current_group())
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


def answers(request, question_id=''):
    if request.method == 'POST':
        g = Group.objects.get(name=request.POST.get("group"))
        set_current_group(g)

    template = loader.get_template('answers.html')

    qs = Question.objects.order_by('-question_number').reverse()

    req_group = request.GET.get('group')
    if req_group is None:
        group = get_current_group()
    else:
        group = Group.objects.get(name=req_group)
        if group is None:
            return HttpResponse('Group not found')

    q = None
    answers = []
    if len(question_id) > 0:
        q = Question.objects.get(question_number=question_id)
        all_answers = Answer.objects.filter(question=q, group=group)
        users = set([a.user for a in all_answers])

        for user in users:
            answers_by_user = Answer.objects.filter(user=user, question=q, group=group)
            answers.append(answers_by_user.last())

    groups = Group.objects.all()

    context = {
        'question_list': qs,
        'question': q,
        'answers': answers,
        'groups': groups,
        'current_group': get_current_group(),
        'shown_group': group
    }

    return HttpResponse(template.render(context, request))
