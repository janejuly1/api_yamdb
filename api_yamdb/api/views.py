from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TokenObtainPairCustomSerializer


class TokenObtainPairCustomView(TokenObtainPairView):
    serializer_class = TokenObtainPairCustomSerializer
