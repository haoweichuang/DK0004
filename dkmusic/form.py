from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment


class UserRegistraionForm(forms.ModelForm):
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='重复密码',
                                widget=forms.PasswordInput)
    username = forms.CharField(label='用户名',
                               help_text="150个字符以内（仅支持字母、数字 @ + . - _）")
    email = forms.EmailField(label='Email地址')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次输入的密码不一致！')
        return cd['password2']


class AddPostForm(forms.ModelForm):
    class Meta:
        model =  Post
        fields = ('name', 'description', 'genre', 'audio_file')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
