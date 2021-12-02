import random
import string

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import (Category, Comment, ConfirmationCode, Genre, Review,
                            Titles, User)

from .permissions import IsAuthorOrReadOnlyPermission, IsAdminPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitlesSerializer,
                          TokenObtainPairCustomSerializer,
                          UserSerializer)


class TokenObtainPairCustomView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairCustomSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            raise ValidationError()

        data = serializer.validated_data

        user = User(username=data['username'], email=data['email'])
        user.save()

        confirmation_code = ConfirmationCode(
            user=user,
            code=''.join(random.choices(
                string.ascii_uppercase + string.digits,
                k=8
            ))
        )
        confirmation_code.save()

        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_object(self):
        if 'username' in self.kwargs and self.kwargs['username'] == 'me':
            return self.request.user

        return super().get_object()

    def get_permissions(self):
        if 'username' in self.kwargs and self.kwargs['username'] == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminPermission]

        return [permission() for permission in permission_classes]


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
