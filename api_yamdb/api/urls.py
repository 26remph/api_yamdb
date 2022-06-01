from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserCreateAPIView, UserViewSet, ConfirmationAPIView

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', UserCreateAPIView.as_view(), name='user_create'),
    path('v1/auth/token/', ConfirmationAPIView.as_view(), name='confirm_user'),
    path('v1/', include(v1_router.urls)),
]
