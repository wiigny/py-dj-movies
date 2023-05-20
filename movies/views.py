from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from _project.pagination import CustomPageNumberPagination
from movies.permissions import CustomPermission
from movies.serializers import MovieSerializer, MovieOrderSerializer
from movies.models import Movie


class MovieView(APIView, CustomPageNumberPagination):
    permission_classes = [CustomPermission]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        pagination = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(instance=pagination, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(serializer.validated_data, request)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    permission_classes = [CustomPermission]

    def get(self, request: Request, id_movie) -> Response:
        movie = get_object_or_404(Movie, id=id_movie)

        movie.added_by = movie.user.email

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, id_movie) -> Response:
        movie = get_object_or_404(Movie, id=id_movie)

        movie.delete()

        return Response(None, status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id_movie: int):
        movie = get_object_or_404(Movie, id=id_movie)

        serializer = MovieOrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(serializer.validated_data, movie, request)

        return Response(serializer.data, status.HTTP_201_CREATED)
