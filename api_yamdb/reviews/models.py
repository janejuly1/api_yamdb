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
    role = models.CharField(max_length=20,


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
