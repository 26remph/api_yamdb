from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from reviews.models import Comment, Review, User

from .serializers import CommentSerializer, ReviewSerializer


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

