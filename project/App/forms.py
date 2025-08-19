from django import forms
from .models import Posts
from .models import Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'image', 'content', 'category', 'status', 'main_post']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control','rows': 3,'placeholder': 'Write your comment...'})}
