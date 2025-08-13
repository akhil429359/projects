from django import forms
from .models import Posts

class BlogForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'image', 'content', 'category', 'section', 'status', 'main_post']
