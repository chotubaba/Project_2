from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    '''
    Generate a form based on the User model with the fields:
    username, email, password1, password2
    '''
    # CUSTOMISE SAVE METHOD TO INCLUDE 'EMAIL' FIELD
    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user