from django.contrib import admin
from django.contrib.auth.models import User,Group
from .models import User_profile

class Profile_inline(admin.StackedInline):
    model = User_profile


class User_model(admin.ModelAdmin):
    model = User
    list_display = ('username','date_joined','last_login','is_staff','is_superuser')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [Profile_inline]

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, User_model)


 