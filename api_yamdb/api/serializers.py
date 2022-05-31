from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Comment, Review, User


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass
