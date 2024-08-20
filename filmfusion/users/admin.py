from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP

class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'otp', 'created_at')
    search_fields = ('user__email', 'otp')
    list_filter = ('created_at',)

# class UserAdmin(BaseUserAdmin):
#     list_display = ('id', 'email', 'name', 'is_staff', 'is_active', 'date_joined')
#     list_filter = ('is_staff', 'is_active', 'date_joined')
#     search_fields = ('email', 'name')
    # ordering = ('email',)

#     def save_model(self, request, obj, form, change):
#         if 'password' in form.cleaned_data:
#             obj.set_password(form.cleaned_data['password'])
#         super().save_model(request, obj, form, change)

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('email', 'name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    filter_horizontal = ('user_permissions',)
    ordering = ('email',)


    def save_model(self, request, obj, form, change):
        if not change:  
            if 'password1' in form.cleaned_data:
                obj.set_password(form.cleaned_data['password1'])
        else:
            if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
                obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(OTP, OTPAdmin)