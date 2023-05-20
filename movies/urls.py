from django.urls import path
from movies.views import MovieView, MovieDetailView, MovieOrderView


urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:id_movie>/", MovieDetailView.as_view()),
    path("movies/<int:id_movie>/orders/", MovieOrderView.as_view()),
]
