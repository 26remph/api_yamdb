from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


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
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки категории"""

    class Meta:
        fields = ('name', 'slug')
        model = Category

    def create(self, validated_data):
        print('validated_data=', validated_data)
        return None


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки жанров"""

    class Meta:
        fields = ('name', 'slug')
        model = Genre

    def create(self, validated_data):
        print('validated_data=', validated_data)
        return None


class GenreReadWriteField(serializers.Field):

    def to_representation(self, value):
        print('to_representation - > ', '-' * 50)
        print('self=', self)
        print('dir=', dir(self))
        print('value=', value)
        # value = {'slug': 'unknown'}

        return value

    def to_internal_value(self, data):
        print('to_internal_value - > ', '-' * 50)
        print('self=', self)
        print('data=', data)
        return data


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для упаковки произведений"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )
        model = Title

    def get_rating(self, obj):
        return 0

    def validate(self, data):
        print('validate - > ', '-' * 50)
        print('validate self=', self)
        print('validate initial_data=', self.initial_data)
        print('validate data=', data)
        print('type data=', data)
        # --------

        if not (init_genre := self.initial_data.get('genre')):
            raise ValidationError(
                '`genre` field: This field is required.'
            )
        if not(isinstance(init_genre, list)):
            raise ValidationError(
                f'`genre`: Invalid data. Expected a list, '
                f'but got `{type(init_genre)}`. '
            )

        for slug in init_genre:
            if not Genre.objects.filter(slug=slug).exists():
                raise ValidationError(
                    f'`genre`: Does not exist slug str `{slug}`.'
                )

        data['genre'] = init_genre

        if not (init_category := self.initial_data.get('category')):
            raise ValidationError(
                '`category`: This field is required.'
            )

        if not Category.objects.filter(slug=init_category).exists():
            raise ValidationError(
                f'`category`: Does not exist slug str `{init_category}.`'
            )

        data['category'] = Category.objects.get(slug=init_category)

        return data

    # def validate_genre(self, value):
    #     """Нормализует входящие данные для записи в базу данных"""
    #     print('validate_genre - > ', '-' * 50)
    #     print('self=', self)
    #     print('value=', value)
    #
    #     if not(isinstance(value, list)):
    #         raise ValidationError(
    #             f"Invalid data. Expected a list, but got `{type(value)}`."
    #         )
    #     normalize_data = []
    #     genre_dict = {}
    #     for elem in value:
    #         if not (isinstance(elem, str)):
    #             raise ValidationError(
    #                 f"Invalid data. Expected a `str`, but got `{type(elem)}`."
    #             )
    #         try:
    #             genre_obj = Genre.objects.get(slug=elem)
    #         except Genre.DoesNotExist:
    #             raise ValidationError(
    #                 f"Slug genre category `{elem}` does not exists."
    #             )
    #
    #         genre_dict['name'] = genre_obj.name
    #         genre_dict['slug'] = genre_obj.slug
    #
    #         if genre_dict in normalize_data:
    #             raise ValidationError(
    #                 f"Data not unique `{value}`"
    #             )
    #
    #         normalize_data.append(genre_dict.copy())
    #
    #     return normalize_data

    def get_genre(self, obj):
        print('get_genre - > ', '-' * 50)
        print('self=', self)
        print('obj=', obj)
        return obj

    def create(self, validated_data):
        print('CREATE ->', '-' * 50)
        print('validated_data=', validated_data)
        print('validated_data type=', type(validated_data))
        print('self create =', self)

        # raise ValidationError('DEBUG stop')
        # genres = validated_data.get('genre')
        genres = validated_data.pop('genre')
        print('pop validated_data=', validated_data)
        print('genres=', genres)

        title, status = Title.objects.get_or_create(**validated_data)
        print('title=', title)
        print('title=', status)
        genre = Genre.objects.filter(slug__in=genres)
        print('genre=', genre)
        title.genre.set(genre)

        return title


class GenreTitles(serializers.ModelSerializer):

    class Meta:
        fields = ('title', 'genre')
        model = GenreTitle


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
