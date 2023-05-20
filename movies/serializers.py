from rest_framework import serializers
from movies.models import Movie, textRating, MovieOrder
import ipdb


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=127)
    synopsis = serializers.CharField(required=False)
    duration = serializers.CharField(
        max_length=10,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    rating = serializers.ChoiceField(
        default=textRating.G,
        choices=textRating.choices,
    )

    added_by = serializers.CharField(read_only=True)

    def save(self, validated_data, request):
        movie = Movie.objects.create(**validated_data, user=request.user)
        self.validated_data["added_by"] = request.user.email
        self.validated_data["id"] = movie.id
        self.validated_data["synopsis"] = movie.synopsis
        return movie


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.EmailField(read_only=True)
    buyed_at = serializers.CharField(read_only=True)

    def save(self, validated_data, movie, request):
        order = MovieOrder.objects.create(
            movie=movie,
            user=request.user,
            **validated_data,
        )
        self.validated_data["id"] = order.id
        self.validated_data["title"] = movie.title
        self.validated_data["buyed_by"] = request.user.email
        self.validated_data["buyed_at"] = order.buyed_at

        return self.validated_data
