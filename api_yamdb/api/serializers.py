from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import (Category, Comment,
                            Genre, Review,
                            Title, User,
                            ConfirmationCode)


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
    username = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(required=False, choices=User.ROLE)

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
        model = User

    def validate(self, attrs):
        if 'request' in self.context:
            request = self.context['request']
            user = request.user
            if (user.is_authenticated
                    and user.role != 'admin'
                    and not user.is_superuser
                    and 'role' in attrs):
                attrs['role'] = user.role

        return super().validate(attrs)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())])

    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())])

    def validate(self, attrs):
        if 'username' in attrs and attrs['username'] == 'me':
            raise ValidationError({'username': 'username cannot be me'})

        return super().validate(attrs)


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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(slug_field='slug',
                       queryset=Genre.objects.all(), many=True)
    category = CategoryField(slug_field='slug',
                             queryset=Category.objects.all(), required=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    # def get_rating(self, obj):
    #     return Titles.objects.annotate(avg_rating=Avg('review__score')).order_by('-avg_score')


class CurrentTitleDafault:
    requires_context = True

    def __call__(self, serializer_field):
        c_view = serializer_field.context['view']
        title_id = c_view.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.HiddenField(default=CurrentTitleDafault())
    # author = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only=True
    # )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = (UniqueTogetherValidator(
            queryset=Review.objects.all(), fields=('title', 'author')),)

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
