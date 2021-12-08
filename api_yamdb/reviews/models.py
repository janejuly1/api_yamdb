from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE = [('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')]

    first_name = models.CharField(_('first name'), max_length=150,
                                  null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=150,
                                 null=True, blank=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE,
                            default='user', null=False, blank=True)


class ConfirmationCode(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='code')
    code = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'code'],
                name='unique_user_code'
            )
        ]


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='titles'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(
        'Оценка', validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
