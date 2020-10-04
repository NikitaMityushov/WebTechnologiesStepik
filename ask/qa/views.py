from django.shortcuts import render
from django.core.paginator import Paginator
from qa.models import Question, Answer


# Create your views here.
from django.http import HttpResponse 

def test(request, *args, **kwargs):
    return HttpResponse('OK')


def display_new_question(request, *args, **kwargs):
    question_list = Question.objects.all().order_by("-id")
    paginator = Paginator(question_list, 10)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, "index.html", {'questions': questions})


def display_popular(request, *args, **kwargs):
    question_list = Question.objects.popular().order_by("-rating")
    paginator = Paginator(question_list, 10)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, "index.html", {'questions': questions})


def display_concrete(request, req_id):
    question = Question.objects.filter(id=req_id).first()
    answers = Answer.objects.filter(question=question)
    return render(request, "con_ques.html", {'question': question}, {'answers': answers})
