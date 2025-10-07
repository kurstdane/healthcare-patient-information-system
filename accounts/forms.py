from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']