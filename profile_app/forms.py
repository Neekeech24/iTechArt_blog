from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.password_validation import validate_password


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean(self):
        super().clean()
        user = self.instance
        try:
            validate_password(self.cleaned_data['password'], user=user)
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                self.add_error('password','Введенные пароли не совпадают.')
            return self.cleaned_data
        except KeyError:
            return self.cleaned_data

