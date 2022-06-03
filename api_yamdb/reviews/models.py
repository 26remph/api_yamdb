from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug категории',
    )

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель для работы с жанрами произведений"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug жанра',
    )

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель для работы с произведениями"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Укажите категорию произведения'
    )

    def __str__(self):
        return self.name[:SLICE_REVIEW]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genretitles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genretitles',
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Модель для работы с отзывами на произведения"""
    ONE, TWO, THREE, FOUR, FIVE = 1, 2, 3, 4, 5
    SIX, SEVEN, EIGHT, NINE, TEN = 6, 7, 8, 9, 10

    ANSWER_CHOICES = [
        (ONE, '1'), (TWO, '2'), (THREE, '3'), (FOUR, '4'), (FIVE, '5'),
        (SIX, '6'), (SEVEN, '7'), (EIGHT, '8'), (NINE, '9'), (TEN, '10')
    ]

    score = models.IntegerField(choices=ANSWER_CHOICES, default=FIVE)
    title = models.ForeignKey(
        Title,
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
        # auto_now_add=True,
        # db_index=True,
        default=timezone.now,
    )

    class Meta:
        ordering = ('-pub_date',)
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
    pub_date = models.DateTimeField(
        'Дата комментария',
        # auto_now_add=True
        default=timezone.now,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text[:SLICE_REVIEW]
