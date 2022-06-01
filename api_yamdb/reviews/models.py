from django.contrib.auth.models import AbstractUser
from django.db import models

SLICE_REVIEW = 30


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Доп.поля: Био, Роль, Код подтверждения.
    Методы: is_moderator, is_admin
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=255,
        choices=USER_ROLES,
        default=USER,
        db_index=True
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def is_moderator(self):
        return self.role == User.MODERATOR

    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    def __str__(self):
        return str(self.username)


class Category(models.Model):
    """Модель для работы с категориями произведений"""
    title = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug категории',
    )

    def __str__(self):
        return self.title


class Genre(models.Model):
    """Модель для работы с жанрами произведений"""
    title = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug жанра',
    )

    def __str__(self):
        return self.title


class Title(models.Model):
    """Модель для работы с произведениями"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    ),
    year = models.IntegerField('Год выпуска'),
    description = models.TextField(),
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Укажите жанр произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Укажите категорию произведения'
    )


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='GenreTitles',
        verbose_name='Жанр произведения',
        help_text='Укажите жанр произведения',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='GenreTitles'
    )


class Review(models.Model):
    """Модель для работы с отзывами на произведения"""
    ONE, TWO, THREE, FOUR, FIVE = 1, 2, 3, 4, 5
    SIX, SEVEN, EIGHT, NINE, TEN = 6, 7, 8, 9, 10

    ANSWER_CHOICES = [
        (1, ONE), (2, TWO), (3, THREE), (4, FOUR), (5, FIVE),
        (6, SIX), (7, SEVEN), (8, EIGHT), (9, NINE), (10, TEN)
    ]

    score = models.IntegerField(choices=ANSWER_CHOICES, default=FIVE)
    title = models.ForeignKey(
        "Title",
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзывы',
        help_text='Отзыв на творческое произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Расскажите что вы думаете об этом.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор произведения',
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
        db_index=True,

    )

    class Meta:
        ordering = ['title'],
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы'

        indexes = [
            models.Index(fields=['author', 'title'], name='author_title'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_title'
            )
        ]

    def __str__(self):
        return self.text[:SLICE_REVIEW]


class Comment(models.Model):
    """Модель для работы с комментариями на отзывы"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    created = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:SLICE_REVIEW]
