from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from user.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "phone", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]
        self.fields["email"].required = True


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone", "country", "avatar"]


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs.update({"placeholder": "Email"})
