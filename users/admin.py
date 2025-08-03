from django.contrib import admin
from users.models import Custom_User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(Custom_User)
class CustomUserAdmin( UserAdmin ):
    model = Custom_User
    fieldsets = (
        (None, {'fields': ('username', 'password') }),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_image') }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions') }),
        ("Important Date's", {'fields': ('last_login', 'date_joined') })  
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'bio', 'profile_image')
        })
    )

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email'
    )

    ordering = (
        '-username',
    )