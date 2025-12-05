from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, EmailOTP, MFADevice


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "phone",
        "is_verified",
        "has_mfa",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = ("role", "is_verified", "has_mfa", "is_staff", "is_active", "date_joined")

    ordering = ("email",)

    search_fields = ("email", "first_name", "last_name", "role", "phone")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Custom Fields", {
            "fields": (
                "role",
                "is_verified",
                "has_mfa",
            ),
        }),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "first_name", "last_name"),
            },
        ),
        ("Custom Fields", {
            "fields": (
                "role",
                "phone",
                "is_verified",
                "has_mfa",
            ),
        }),
    )

    readonly_fields = ("date_joined", "last_login")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "location", "phone", "created_at", "updated_at")
    search_fields = ("user__email", "full_name", "location")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        (None, {"fields": ("user",)}),
        ("Profile Information", {
            "fields": ("full_name", "bio", "phone", "location", "profile_image")
        }),
        ("Professional Details", {
            "fields": ("skills", "experience")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ("email", "purpose", "otp", "created_at", "expires_at", "attempts", "is_expired_display")
    search_fields = ("email", "purpose")
    list_filter = ("purpose", "created_at", "expires_at")
    readonly_fields = ("created_at", "expires_at", "attempts")
    
    def is_expired_display(self, obj):
        return "Yes" if obj.is_expired() else "No"
    is_expired_display.short_description = "Expired"
    is_expired_display.boolean = True


@admin.register(MFADevice)
class MFADeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "confirmed", "created_at")
    search_fields = ("user__email",)
    list_filter = ("confirmed", "created_at")
    readonly_fields = ("created_at",)
    
    fieldsets = (
        (None, {"fields": ("user",)}),
        ("MFA Settings", {
            "fields": ("secret", "confirmed")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )




# Admin registrations have been moved to auth_service.src.domain.admin
# to avoid conflicts and ensure proper configuration
