from django.contrib.auth import authenticate
from django.db.models import Avg
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Category, Comment, Genre, Review, Titles, User


class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()
        self.fields.pop('password')

    def validate(self, attrs):
        authenticate_kwargs = {
            'username': attrs['username'],
            'confirmation_code': attrs['confirmation_code'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        data = {}
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
        model = User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     allow_null=False,
                                     allow_blank=False)

    email = serializers.EmailField(required=True,
                                   allow_null=False,
                                   allow_blank=False)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Category


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreField(slug_field='slug',
                       queryset=Genre.objects.all(), many=True)
    category = CategoryField(slug_field='slug',
                             queryset=Category.objects.all(), required=False)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Titles
        fields = '__all__'

    # def get_rating(self, obj):
    #     return Titles.objects.annotate(avg_rating=Avg('review__score')).order_by('-avg_score')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        required=False,
        queryset=Titles.objects.all()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review

    # def get_score(self, obj):
    #     return Titles.objects.annotate(avg_rating=Avg('review__score')).order_by('-avg_score')


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='id',
        # many=True,
        required=False,
        queryset=Review.objects.all()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
