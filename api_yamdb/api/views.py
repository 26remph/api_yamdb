from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.decorators import action
from rest_framework import filters, viewsets, status, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review, User, Category, Genre, Title
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import AdminOnly

from .mixins import (
    PostDeleteByAdminOrReadOnlyMixin,
    PostDeletePatchByAdminOrReadOnlyMixin
)


from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    UserSerializer,
    UserCreateSerializer,
    ConfirmationSerializer
)


class CategoryViewSet(PostDeleteByAdminOrReadOnlyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(PostDeleteByAdminOrReadOnlyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(PostDeletePatchByAdminOrReadOnlyMixin):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('Category__slug', 'Genre__slug', 'name', 'year',)


class CommentViewSet(viewsets.ModelViewSet):
    """Вью сет для работы с комментариями."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вью сет для работы с отзывами"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def me(self, request):
        """
        Функция управления собственным аккаунтом.
        """
        if request.method.lower() == 'get':
            serializer = UserSerializer(instance=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            if (
                'role' in serializer.validated_data
                and not request.user.is_admin
            ):
                serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(APIView):
    """
    Класс для создания нового пользователя
    """
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            if not User.objects.filter(
                username=serializer.validated_data['username']
            ).exists():
                serializer.save(role='user')
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
            user.confirmation_code = str(RefreshToken.for_user(user))
            user.save(update_fields=['confirmation_code'])
            send_mail(
                'Confirmation code.',
                user.confirmation_code,
                'no_replay@yambd.ru',
                [user.email, ],
                fail_silently=False,
            )
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmationAPIView(APIView):
    """
    Класс для получения токена по конфирмейшн коду.
    """
    def post(self, request, *args, **kwargs):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
            user.confirmation_code = ''
            user.save(update_fields=['confirmation_code'])
            return Response(
                {'token':
                 str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
