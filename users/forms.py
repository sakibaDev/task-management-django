import re
from django import forms
from django.contrib.auth.models import User
from tasks.forms import StyledFormMixin

class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Check password length
        if len(password) < 8:
            raise forms.ValidationError('Your password must be at least 8 characters long.')

        # Check for at least one uppercase, one lowercase, one digit, and one special character
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('Password must contain at least one special character.')

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
