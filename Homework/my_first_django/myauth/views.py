from random import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test,)
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page

from .models import Profile
from .forms import ProfileEditForm


def start_myauth(request: HttpRequest) -> HttpResponse:
    return render(request, "myauth/base.html")


#@login_required
#def about_me(request):
#    profile = request.user.profile
#
#    if request.method == "POST":
#        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
#        if form.is_valid():
#            form.save()
#            return redirect("about-me")
#        else:
#            form = ProfileEditForm(instance=profile)
#
#        return render(request,
#                      "about-me.html",
#                      {"form": form, "profile": profile,})


class AboutMeView(UpdateView):
    model = Profile
    #fields = ("avatar",)
    form_class = ProfileEditForm
    template_name_suffix = "_update_avatar_form"
    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset = None):
        # print(f" текущий пользователь {self.request.user.profile.pk}\n {self.request.user}")
        # print(f"object {Profile.objects}")
        return  self.request.user.profile


#class AboutMeView(TemplateView):
#    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class UsersListView(ListView):
    template_name = "myauth/users_list.html"
    queryset = User.objects.select_related().all()
    context_object_name = "users"


class UserDetail(DetailView):
    template_name = "myauth/user_detail.html"
    queryset = User.objects.select_related().prefetch_related().all()
    context_object_name = "user"


class ProfileUpdate(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.pk == self.get_object().user.pk
    model = Profile
    #fields = ("avatar",)
    template_name_suffix = "_update_form"
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse(
            "myauth:user_detail",
            kwargs={"pk": self.object.user.pk},
        )

