from django import forms
from .models import Articles, Comments
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    """Форма добавления статьи"""
    class Meta:
        model = Articles
        fields = ('name', 'text')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    """Форма авторизации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    # Нужно переопределить метод save для пользователя, потому что по умолчанию нужно
    # хэшировать пароли, а не просто их туда строкой сохранять.
    # Этот метод основан на методе save класса UserCreationForm из django.contrib.auth.forms.py
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    """Форма добавления комментария"""
    class Meta:
        model = Comments
        fields = ('text',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['text'].widget = forms.Textarea(attrs={'rows': 5})
