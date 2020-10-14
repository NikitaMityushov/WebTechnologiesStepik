from django.shortcuts import render, get_object_or_404, Http404, HttpResponseRedirect, redirect
from django.core.paginator import Paginator, EmptyPage
from qa.models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from qa.forms import AnswerForm, AskForm, AuthorizationForm, SignupForm
from datetime import datetime, timedelta
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
    # POST
    if request.method == "POST":
        if request.user.is_authenticated:
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save()
                answer.author = request.user
                answer.save()
                url = answer.question.get_url()
                return HttpResponseRedirect(url)
        # is_authentificated == False
        return HttpResponseRedirect("/login/")
    # GET
    question = get_object_or_404(Question, id=req_id,)
    answers = Answer.objects.filter(question = question)
    form = AnswerForm(initial={'question': req_id})
    print(form)
    return render(request, 'con_ques.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })


def fill_db():
    user, _ = User.objects.get_or_create(                                                                                                        
        username='x',                                                                                                                            
        defaults={'password':'y', 'last_login': datetime.now()})

    for i in range(0, 30):
        title = 'question' + str(i)
        text = 'text' + str(i)
        author = user
        rating = 0 + i
        Question.objects.create(title=title, text=text, author=author, rating=rating)

    Question.objects.create(title='question last', text='text', author=user)  
    Question.objects.get_or_create(pk=3141592, title='question about pi', text='what is the last digit?', author=user)


def post_question(request):
    # POST
    if request.method == "POST":
        if request.user.is_authenticated:
            print("authorized111")
            form = AskForm(request.POST)
            print(request.POST)
            if form.is_valid():
                print("valid")
                question = form.save()
                question.author = request.user
                question.save()
                url = question.get_url()
                return HttpResponseRedirect(url)
        else:
            # is_authentificated == False
            print("not authorized 222")
            return HttpResponseRedirect("/login/")
    # GET
    form = AskForm()
    return render(request, 'post_question.html', {'form': form})


def authorization(request):
    # POST
    if request.method == "POST":
        form = AuthorizationForm(request.POST)
        print("POST")
        print(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            print(username)
            password = form.cleaned_data.get("password")
            print(password)
            user = User.objects.get(username=username, password=password) 
            if user is not None:
                print("valid user")
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    print("error message") # peredelat'
                    return HttpResponseRedirect("login.html")
            else:
                print("the user is not defined")

        else:
            print("invalid form!!")

    # GET
    form = AuthorizationForm()
    return render(request, "login.html", {"form": form})


def post_answer(request):
    pass 


def signup(request):
    form = SignupForm(request.POST or None)
    
    if form.is_valid():
        try:
            user = form.save()
        except:
            user = None

        if user != None:
            logout(request)
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            request.session["register_error"] = 1

    return render(request, "signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/") 
