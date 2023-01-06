from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer
from .serializers import TokenSerializer
from .serializers import MovieSerializer
from .serializers import GenreSerializer
from .serializers import CommentSerializer
from .serializers import ChangePasswordSerializer
from .serializers import ChangeNameSerializer

from .models import UserData
from .models import Movie
from .models import Genre
from .models import Comment


# Create your views here.


# view for registering users
class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(TokenObtainPairView):
    serializer_class = TokenSerializer


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = UserData

    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeNameView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangeNameSerializer
    model = UserData

    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.name = serializer.data.get("new_name")
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieView(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    # # noinspection PyUnresolvedReferences
    # queryset = Movie.objects.all()

    def get_queryset(self):
        # noinspection PyUnresolvedReferences
        queryset = Movie.objects.all()

        movie_id = self.request.query_params.get('movie_id')
        genre_id = self.request.query_params.get('genre_id')
        name = self.request.query_params.get('name')

        if genre_id is not None:
            queryset = queryset.filter(genre_id=genre_id)

        if name is not None:
            queryset = queryset.filter(name=name)

        if movie_id is not None:
            queryset = queryset.filter(id=movie_id)

        return queryset


class GenreView(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    # noinspection PyUnresolvedReferences
    queryset = Genre.objects.all()


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # noinspection PyUnresolvedReferences
    queryset = Comment.objects.all()


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # noinspection PyUnresolvedReferences
    queryset = UserData.objects.all()
