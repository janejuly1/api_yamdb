from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractBaseUser):
    ROLE = [('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. '
                    'Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    user_bio = models.TextField(null=True, blank=True)
    user_role = models.CharField(max_length=20,
                                 choices=ROLE,
                                 default='user',
                                 null=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


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
