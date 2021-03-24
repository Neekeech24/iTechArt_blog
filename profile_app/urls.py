from django.contrib.auth import urls
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from .views import user_profile, delete_profile, ProfileView, RegistraionView

urlpatterns = [
    path('', include(urls)),
    path('profile/', user_profile, name='user_profile'),
    path('profile/<pk>', login_required(ProfileView.as_view()), name='profile_detail'),
    path('delete_profile', delete_profile, name='delete_profile'),
    path('registration', RegistraionView.as_view(), name='registration')
]
