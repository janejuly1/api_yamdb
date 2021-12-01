import random
import string

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Comment, ConfirmationCode, Review, Titles, User

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (CommentSerializer, RegistrationSerializer,
                          ReviewSerializer, TokenObtainPairCustomSerializer)


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('titl_id')
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
