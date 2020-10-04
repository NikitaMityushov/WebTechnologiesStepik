from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage
from qa.models import Question, Answer
from django.contrib.auth.models import User
import datetime


# Create your views here.
from django.http import HttpResponse 

def test(request, *args, **kwargs):
    return HttpResponse('OK')


def display_new_question(request, *args, **kwargs):
    # fill_db()
    tags = Question.objects.new()
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 10:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(tags, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    paginator.baseurl = '?page='

    return render(request, 'display_new.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def display_popular(request, *args, **kwargs):
    tags = Question.objects.popular()
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 10:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(tags, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    paginator.baseurl = '?page='

    return render(request, 'display_popular.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def display_concrete(request, req_id):
    question = get_object_or_404(Question, id=req_id)
    return render(request, 'con_ques.html', {
        'question': question,
    })


def fill_db():
    user, _ = User.objects.get_or_create(                                                                                                        
        username='x',                                                                                                                            
        defaults={'password':'y', 'last_login': datetime.datetime.now()})

    for i in range(0, 30):
        title = 'question' + str(i)
        text = 'text' + str(i)
        author = user
        rating = 0 + i
        Question.objects.create(title=title, text=text, author=author, rating=rating)

    Question.objects.create(title='question last', text='text', author=user)  
    Question.objects.get_or_create(pk=3141592, title='question about pi', text='what is the last digit?', author=user)
