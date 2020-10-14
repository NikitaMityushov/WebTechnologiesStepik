from qa.models import Question, Answer
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    author = forms.IntegerField(widget=forms.HiddenInput)

    
    def clean_text(self):
        question = self.cleaned_data['text']
        print(self.cleaned_data)
        if question == '':
            raise forms.ValidationError('The text is empty')
        else:
            return question

    def clean_title(self):
        tl = self.cleaned_data['title']
        if tl == '':
            raise forms.ValidationError('The title is empty')
        else:
            return tl
        
    def save(self):
        self.cleaned_data['author'] = get_object_or_404(User, pk=self.cleaned_data['author'])
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)
    author = forms.IntegerField(widget=forms.HiddenInput)

    def clean_text(self):
        answer = self.cleaned_data['text']
        print(answer)
        return answer

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(Question, pk=self.cleaned_data['question'])
        self.cleaned_data['author'] = get_object_or_404(User, pk=self.cleaned_data['author'])
        print(self.cleaned_data)
        answer = Answer(**self.cleaned_data)                
        answer.save()
        return answer


class AuthorizationForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_username(self):
        login = self.cleaned_data.get("username")
        user = User.objects.filter(username=login)

        if not user.exists():
            print("login")
            raise forms.ValidationError("This is invalid user")

        return login
    
    def clean_password(self):
        password = self.cleaned_data.get("password")

        if password == "":
            print("password")
            raise forms.ValidationError("This is incorrect password")

        return password



class SignupForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.Textarea)
    email = forms.EmailField(label="email", widget=forms.Textarea)
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    def clean_username(self):
        login = self.cleaned_data.get("username")
        user = User.objects.filter(username=login)
        
        if user.exists():
            raise forms.ValidationError("Such user is already exists")

        return login

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("This is an invalid email, please pick another.")
        
        return email


    def clean_password(self):
        password = self.cleaned_data['password']
        
        if password == "":
            raise forms.ValidationError("Incorrect password")
        else:
            return password    

    def save(self):
        user = User.objects.create(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        return user

