from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TokenObtainPairCustomSerializer


class TokenObtainPairCustomView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairCustomSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
