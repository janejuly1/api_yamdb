from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet


app_name = 'api'
v1_router = DefaultRouter()
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comments')
# urlpatterns = [
#     path('v1/', include(v1_router.urls)),
#     path('v1/auth/token/', views.obtain_auth_token),
# ]
