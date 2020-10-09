from qa.models import Question, Answer
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    
    def clean_question(self):
        question = self.cleaned_data['question']
        if question == '':
            raise forms.ValidationError('Question is empty')
        else:
            return question
        

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_answer(self):
        answer = self.cleaned_data['answer']
        return answer

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(Question, pk=self.cleaned_data['question'])
        answer = Answer(text=self.cleaned_data['text'],
                        question=self.cleaned_data['question'])
        answer.save()
        return answer

