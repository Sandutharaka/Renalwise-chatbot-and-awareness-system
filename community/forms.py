# community/forms.py

from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your post here...', 'class': 'form-control'}))
    
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write a comment...', 'class': 'form-control'}))
    
    class Meta:
        model = Comment
        fields = ['content']
