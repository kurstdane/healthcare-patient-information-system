from django import forms
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class ForcePasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'contact_number', 'profile_picture']