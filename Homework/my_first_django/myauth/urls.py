from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (start_myauth,
                    get_cookie_view,
                    set_cookie_view,
                    set_session_view,
                    get_session_view,
                    logout_view,
                    MyLogoutView,
                    AboutMeView,
                    RegisterView,

                    UsersListView,
                    UserDetail,
                    ProfileUpdate,
                    #about_me,
                    )

app_name = "myauth"

urlpatterns = [
    path("", start_myauth, name="start-myauth"),
    # path("login/", login_view, name="login"),
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"),
    path("logout/", logout_view, name="logout"),
    # path("logout/", MyLogoutView.as_view(), name="logout"),

    path("about-me/", AboutMeView.as_view(), name="about-me"),
    # path("about-me/", about_me, name="about-me"),

    path("register/", RegisterView.as_view(), name="register"),

    path("users/", UsersListView.as_view(), name="users_list"),
    path("users/<int:pk>", UserDetail.as_view(), name="user_detail"),
    path("user/<int:pk>/update", ProfileUpdate.as_view(), name="profile_update"),


    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
]
