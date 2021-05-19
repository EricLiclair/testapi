from django.urls import path
from .views import *

# docs
urlpatterns = [
    path('create-profile', CreateProfileView.as_view()),
    path('profiles', ListProfileView.as_view()),
    path('get-profile/<str:id>', GetProfileView.as_view()),
    path('update-profile/<str:id>', UpateProfileView.as_view()),
    path('', testview),
]
