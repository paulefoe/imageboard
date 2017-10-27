from django import forms
from .models import Post


class OpForm(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = Post
        fields = ['email', 'name', 'title', 'text', 'image']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['email', 'name', 'title', 'text', 'image']
        labels = {
            'email': 'Опции',
            'name': 'Имя',
            'title': 'Тема',
            'text': 'Пост',
            'image': 'Картинка'
        }

