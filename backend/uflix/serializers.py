# import serializers from the REST framework
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# import the test data model
from .models import UserData
from .models import Movie
from .models import Genre
from .models import Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        data['id'] = self.user.id
        data['name'] = self.user.name
        data['email'] = self.user.email
        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = UserData

    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField(required=True)


class ChangeNameSerializer(serializers.Serializer):
    model = UserData

    """
    Serializer for password change endpoint.
    """
    new_name = serializers.CharField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user_id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'user_name', 'movie_id', 'text')


class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(source='genre_id', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'poster',
                  'genre_id', 'genre', 'score', 'url', 'comments')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')
