from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Movie, Review

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('stars', 'user', 'movie', "desc")

class ReviewMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('stars', "desc")

class MovieSerializer(serializers.ModelSerializer):
    movie_reviews = ReviewMovieSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'desc', 'year', 'img', 'movie_reviews', 'avg_rating')

class MovieMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'img', 'avg_rating')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password' : {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


