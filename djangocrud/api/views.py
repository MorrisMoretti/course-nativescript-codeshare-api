from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MovieSerializer, MovieMiniSerializer, ReviewSerializer, UserSerializer
from .models import Movie, Review


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        movies = Movie.objects.all()
        serializer = MovieMiniSerializer(movies, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if 'movie' in request.data and 'stars' in request.data:
            movie = Movie.objects.get(id=request.data['movie'])
            stars = request.data['stars']
            desc = request.data['desc']

            try:
                my_review = Review.objects.get(movie=movie.id, user=request.user.id)
                my_review.stars = stars
                my_review.desc = desc
                my_review.save()
                serializer = MovieSerializer(movie, many=False)
                response = {"message": "Review updated", "result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                my_review = Review.objects.create(movie=movie, user=request.user, stars=stars, desc=desc)
                serializer = MovieSerializer(movie, many=False)
                response = {"message": "Review created", "result": serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {"message": "You need to pass all params"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        serializer = UserSerializer(user, many=False)
        return Response({'token': token.key, 'user': serializer.data})