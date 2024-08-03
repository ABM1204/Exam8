from django import forms
from .models import Forum, Reply

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
