from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


class PasswordChangeFormRu(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Текущий пароль"
        self.fields["new_password1"].label = "Новый пароль"
        self.fields["new_password2"].label = "Подтверждение нового пароля"
        self.fields["old_password"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "current-password"}
        )
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "new-password"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "new-password"}
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {
            "email": "Электронная почта",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
        }
