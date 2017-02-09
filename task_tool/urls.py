"""task_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import api
from . import views
from . import import_questions


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^import', import_questions.index, name='index'),
    url(r'^questions/(?P<username>[a-z0-9]+)/all', views.all, name='all'),
    url(r'^questions/(?P<username>[a-z0-9]+)/$', views.questions, name='questions'),
    url(r'^questions/(?P<username>[a-z0-9]+)/(?P<question_id>[a-zA-Z0-9]+)', views.questions, name='questions'),
    url(r'^answers/$', views.answers, name='answers'),
    url(r'^answers/(?P<question_id>[a-zA-Z0-9]+)$', views.answers, name='answers'),
]
