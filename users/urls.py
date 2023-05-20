from django.urls import path
from users.views import UserDetailView, UserView, loginJWTView
from rest_framework_simplejwt import views


urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:id_user>/", UserDetailView.as_view()),
    path("users/<int:id_user>/", UserDetailView.as_view()),
    path("users/login/", loginJWTView.as_view()),
    path("users/login/refresh/", views.TokenRefreshView.as_view()),
]
