from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View

from user.forms import CustomAuthenticationForm, UserRegistrationForm, UserUpdateForm
from user.models import User
from user.utils import send_verification_email


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "user/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        send_verification_email(self.object, self.request)
        return response


class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "user/login.html"
    success_url = reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/profile_edit.html"
    context_object_name = "user"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user


class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            messages.success(request, "Email успешно подтвержден!")
            return redirect("login")
        else:
            messages.error(request, "Неверная ссылка подтверждения.")
            return redirect("login")
