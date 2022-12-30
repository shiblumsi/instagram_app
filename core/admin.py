from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name','is_staff']
    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Permissions' ,{'fields':('is_staff','is_active','is_superuser',)}),
        ('Info',{'fields':('name',)}),
        ('Importent Dates',{'fields':('last_login',)})
        )
    
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':(
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_superuser',
                'is_staff',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)

admin.site.register(models.Post)
admin.site.register(models.Comment)