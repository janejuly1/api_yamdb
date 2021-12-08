from django.contrib import admin
from .models import Title, Category, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'category',
        'genre',
        'author',
        'pub_date',
    )
    search_fields = ('name',)
    list_editable = ('genre', 'category', )
    list_filter = ('pub_date', 'category', 'genre', )


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
