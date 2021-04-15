from django import forms
from profile_app.models import UserModel
from django.contrib.auth.password_validation import validate_password
from .tasks import registration_email


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name']


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('username', 'email')

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

