from django.urls import path
from .views import *

urlpatterns = [
    path('users', UserView.as_view()),
    path('get/<str:username>', GetUserView.as_view()),
    path('create', CreateUserView.as_view()),
    path('update/<str:username>', UpdateUserView.as_view()),
    path('login', LoginUserView.as_view()),
    path('logout', LogoutUserView.as_view()),
    path('get-token', GetTokenView.as_view())
]
