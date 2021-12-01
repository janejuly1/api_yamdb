import random
import string

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TokenObtainPairCustomSerializer, RegistrationSerializer
from reviews.models import User, ConfirmationCode


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
