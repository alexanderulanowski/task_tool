from django.http import HttpResponse

from .models import Question, Group


def index(request):
    Question.objects.all().delete()
    q1 = ['1a', '1b', '1c']
    q2 = ['2a', '2b', '2c', '2d']
    q3 = ['3a', '3b', '3c', '3d', '3e', '3f']
    q4 = ['4a', '4b', '4c', '4d', '4e']

    q = [q1, q2, q3, q4]

    for q_ in q:
        for q__ in q_:
            Question(question_number=q__, question_text='<img src="/static/img/{}.png" /><br /><img src="/static/img/{}.png" />'.format(q__[0], q__)).save()

    groups = ['Gruppe 1', 'Gruppe 8']

    groups_db = [g.name for g in Group.objects.all()]

    if set(groups) != set(groups_db):
        for g in groups:
            if not g in groups_db:
                Group(name=g).save()

    groups_db = [g.name for g in Group.objects.all()]

    return HttpResponse("Success. Groups:" + str(groups_db))