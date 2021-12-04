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

##Test
class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category'
    )
    genre = models.ManyToManyField(
        Genre, related_name='genre')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    score = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

# для вьюшки titles, вычесление рейтинга
# from django.db.models import Avg
# Titles.objects.annotate(avg_rating=Avg('reviews__score')).order_by('-avg_score')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
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
