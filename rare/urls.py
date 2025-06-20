"""rare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rareapi.views.auth_view import LoginView, RegisterView, UserListView
from rareapi.views.category import CategoryViewSet
from rareapi.views.comment import CommentViewSet
from rareapi.views.post_view import PostView
from rareapi.views.user_view import CurrentUserView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"posts", PostView, "post")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/me", CurrentUserView.as_view(), name="current-user"),
]
