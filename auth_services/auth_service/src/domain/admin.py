# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# from auth_service.src.domain.models.models import User, UserProfile, EmailOTP, MFADevice


# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = User
#         fields = '__all__'
#         exclude = ('username',)


# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("email",)
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if 'username' in self.fields:
#             del self.fields['username']


# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     model = User
#     form = CustomUserChangeForm
#     add_form = CustomUserCreationForm
    
#     list_display = (
#         "email",
#         "first_name",
#         "last_name",
#         "role",
#         "phone",
#         "is_verified",
#         "has_mfa",
#         "is_staff",
#         "is_active",
#         "date_joined",
#     )
    
#     list_filter = ("role", "is_verified", "has_mfa", "is_staff", "is_active", "date_joined")
    
#     ordering = ("email",)
    
#     search_fields = ("email", "first_name", "last_name", "phone")
    
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
#         (
#             "Permissions",
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         ("Important dates", {"fields": ("last_login", "date_joined")}),
#         ("Custom Fields", {
#             "fields": (
#                 "role",
#                 "is_verified",
#                 "has_mfa",
#             ),
#         }),
#     )
    
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2", "first_name", "last_name"),
#             },
#         ),
#         ("Custom Fields", {
#             "fields": (
#                 "role",
#                 "phone",
#                 "is_verified",
#                 "has_mfa",
#             ),
#         }),
#     )
    
#     readonly_fields = ("date_joined", "last_login")


# @admin.register(UserProfile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "full_name", "location", "phone", "created_at", "updated_at")
#     search_fields = ("user__email", "full_name", "location")
#     list_filter = ("created_at", "updated_at")
#     readonly_fields = ("created_at", "updated_at")
    
#     fieldsets = (
#         (None, {"fields": ("user",)}),
#         ("Profile Information", {
#             "fields": ("full_name", "bio", "phone", "location", "profile_image")
#         }),
#         ("Professional Details", {
#             "fields": ("skills", "experience")
#         }),
#         ("Timestamps", {
#             "fields": ("created_at", "updated_at")
#         }),
#     )


# @admin.register(EmailOTP)
# class OTPAdmin(admin.ModelAdmin):
#     list_display = ("email", "purpose", "otp", "created_at", "expires_at", "attempts", "is_expired_display")
#     search_fields = ("email", "purpose")
#     list_filter = ("purpose", "created_at", "expires_at")
#     readonly_fields = ("created_at", "expires_at", "attempts")
    
#     def is_expired_display(self, obj):
#         return "Yes" if obj.is_expired() else "No"
#     is_expired_display.short_description = "Expired"
#     is_expired_display.boolean = True


# @admin.register(MFADevice)
# class MFAAdmin(admin.ModelAdmin):
#     list_display = ("user", "confirmed", "created_at")
#     search_fields = ("user__email",)
#     list_filter = ("confirmed", "created_at")
#     readonly_fields = ("created_at",)
    
#     fieldsets = (
#         (None, {"fields": ("user",)}),
#         ("MFA Settings", {
#             "fields": ("secret", "confirmed")
#         }),
#         ("Timestamps", {
#             "fields": ("created_at",)
#         }),
#     )
