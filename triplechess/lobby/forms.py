from django.contrib.auth.models import User
import django.forms as forms

_INPUT = {'class': 'form-control'}
_TEXT = {'class': 'form-control', 'autocomplete': 'username'}


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={**_INPUT, 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={**_INPUT, 'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
        widgets = {
            'username': forms.TextInput(attrs={**_TEXT}),
            'email': forms.EmailInput(attrs={**_INPUT, 'autocomplete': 'email'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs=_TEXT),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={**_INPUT, 'autocomplete': 'current-password'}),
    )

