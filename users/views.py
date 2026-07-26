from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from .forms import UserProfileForm, UserRegisterForm
from .models import User
from django.http import HttpResponse

def user_list(request):
    return HttpResponse("Список пользователей")

class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("mailing:home")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("mailing:home")


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
