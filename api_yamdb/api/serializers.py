from rest_framework import serializers, validators
from reviews.models import Comment, Review, User, Category, Genre
from rest_framework.generics import get_object_or_404


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
    """Сериализатор для упаковки категории"""
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки жанров"""
    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки произведений"""
    pass


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделью User
    """
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким именем уже существует.'
            )
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email-адресом уже существует.'
            )
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        lookup_field = 'username'


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя
    """
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    @staticmethod
    def validate_username(username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                {'username':
                 'Использовать имя "me" в качестве username запрещено.'}
            )
        return username

    def validate(self, attrs):
        """
        Валидация username и email.
        Если email и username совпадают, то все ок, делаем запрос на себя
        и получаем токен.
        Если совпадает только что-то одно, то выводим ошибку с инфой.
        """
        if User.objects.filter(username=attrs['username'],
                               email=attrs['email']).exists():
            return attrs
        if (
            User.objects.filter(username=attrs['username']).exists()
            or User.objects.filter(email=attrs['email']).exists()
        ):
            message_dict = {}
            if User.objects.filter(username=attrs['username']).exists():
                message_dict.update(
                    {
                        'username':
                        'Пользователь с именем {} уже есть в базе.'.format(
                            attrs['username']
                        )
                    }
                )
            if User.objects.filter(email=attrs['email']).exists():
                message_dict.update(
                    {
                        'email':
                        'Пользователь с адресом {} уже есть в базе.'.format(
                            attrs['email']
                        )
                    }
                )
            raise serializers.ValidationError(message_dict)
        return attrs

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class ConfirmationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для проверки конфирмейшн кода и выдачи токенов
    """
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if not user.confirmation_code == attrs['confirmation_code']:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения.'}
            )
        return attrs

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
