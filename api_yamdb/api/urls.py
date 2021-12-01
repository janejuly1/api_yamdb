from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet
from .views import TokenObtainPairCustomView

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comments')

urlpatterns = [
    path(
        'v1/auth/token/',
        TokenObtainPairCustomView.as_view(),
        name='token_obtain_pair'
    ),
    # path('v1/', include(v1_router.urls)),
    # path('v1/auth/token/', views.obtain_auth_token),
]
