from django.contrib import admin
from .models import Title, Category, Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'category',
        'author',
        'pub_date',
    )
    search_fields = ('name',)
    list_editable = ('category', )
    list_filter = ('pub_date', 'category', )


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
