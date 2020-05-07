from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo, RecipePost


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

        widget = {
            'username': forms.TextInput(attrs={'class': 'textinputclass'}),
            'email': forms.TextInput(attrs={'class': 'textinputclass'}),
            'password': forms.PasswordInput(attrs={'class': 'textinputclass'})  # check if this will work
        }


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)  # should I add form widget??

        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'imageinputclass'}),
        }


class RecipePostForm(forms.ModelForm):

    class Meta():
        model = RecipePost
        fields = ('author', 'title', 'url', 'image', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'url': forms.URLInput(attrs={'class': 'textinputclass'}),
            'image': forms.ClearableFileInput(attrs={'class': 'imageinputclass'}),
            'text': forms.Textarea(attrs={'class': 'textinputclass'})  # come back and edit this? Check my first clone project
        }
