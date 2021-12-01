from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


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
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Titles(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category'
    )
    genre = models.ForeignKey(
       Genre, on_delete=models.CASCADE, related_name='genre'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    titles = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    score = models.IntegerField(
        default=None, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

# для вьюшки titles, вычесление рейтинга
# from django.db.models import Avg
# Titles.objects.annotate(avg_rating=Avg('reviews__score')).order_by('-avg_score')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'titles'],
                name='unique_author_titles'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
