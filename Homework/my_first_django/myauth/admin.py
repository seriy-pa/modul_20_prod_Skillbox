from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar')
    search_fields = ('user_username', 'bio')
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="150" height="150" />'
        return "No avatar"

    avatar_preview.allow_tags = True
    avatar_preview.short_description = "Avatar Preview"

#admin.site.register(Profile, ProfileAdmin)


