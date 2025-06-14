from django.contrib import admin
from .models import Profile, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ( "first_name", "last_name", "email", "phone","username", "password1", "password2",),
            },
        ),
    )
    list_display = ['username', 'first_name', 'last_name','email', 'phone', 'is_staff']
    list_editable = ['first_name', 'last_name','email', 'phone']
    search_fields = ['username', 'first_name', 'last_name']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly_fields.append('is_superuser')
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and change:
            old_obj = type(obj).objects.get(pk=obj.pk)
        super().save_model(request, obj, form, change)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'address', 'nin', 'bvn']
    list_editable = ['address', 'nin', 'bvn']
    list_display_links = ['user']
    search_fields = ['address', 'nin', 'bvn']




