from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', )
    list_editable = ('role', )
    search_fields = ('username', 'role', )


admin.site.register(User, UserAdmin)
