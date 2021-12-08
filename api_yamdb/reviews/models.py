from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'
    ROLE = [(USER_ROLE, 'user'),
            (MODERATOR_ROLE, 'moderator'),
            (ADMIN_ROLE, 'admin')]

    first_name = models.CharField(max_length=150,
                                  null=True, blank=True)
    last_name = models.CharField(max_length=150,
                                 null=True, blank=True)
    email = models.EmailField(max_length=254)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE,
                            default=USER_ROLE, blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN_ROLE or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE


class ConfirmationCode(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=255)

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
