from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    UserCreateAPIView,
    UserViewSet,
    ConfirmationAPIView,
    CommentViewSet,
    ReviewViewSet,
    GenreViewSet,
    CategoryViewSet
)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register(
    r"titles/(?P<title_id>[^/.]+)/reviews",
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r"titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments",
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/signup/', UserCreateAPIView.as_view(), name='user_create'),
    path('v1/auth/token/', ConfirmationAPIView.as_view(), name='confirm_user'),
    path('v1/', include(v1_router.urls)),
]
