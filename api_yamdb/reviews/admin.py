from django.contrib import admin

from .models import Genre, User, Category


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', )
    list_editable = ('role', )
    search_fields = ('username', 'role', )


class CategorуAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


admin.site.register(Category, CategorуAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(User, UserAdmin)
