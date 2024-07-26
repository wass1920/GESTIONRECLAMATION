from django import forms
from .models import User, Operateur, Claim

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    operateur = forms.ChoiceField(choices=[('orange', 'orange'), ('TT', 'TT')])

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm2(forms.ModelForm):
    class Meta:
        model = Operateur
        fields = ['name', 'email', 'numtel','password']

class ReclamationForm(forms.Form):
    class Meta:
        model = Claim  
        fields = ['text', 'user', 'operator','heure']
