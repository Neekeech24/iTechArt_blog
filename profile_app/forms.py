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

    def clean_password2(self):
        cd = self.cleaned_data
        user = self.instance
        validate_password(cd['password2'], user=user)
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Введенные пароли не совпадают')
        return cd['password2']
