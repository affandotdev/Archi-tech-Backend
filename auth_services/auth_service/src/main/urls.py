from django.contrib import admin
from django.urls import path, re_path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.urls import path


from src.presentation.controllers.profile_controller import (
    UserProfileController,UserProfileUpdateController,UserProfileImageUploadController
)


from src.presentation.controllers.auth_controller import RegisterView
from src.presentation.controllers.otp_controller import VerifyOTPView
from src.presentation.controllers.login_controller import LoginView
from src.presentation.controllers.logout_controller import LogoutView
from src.presentation.controllers.password_controller import ChangePasswordView
from src.presentation.controllers.reset_password_controller import ForgotPasswordView, ResetPasswordConfirmView


# from src.presentation.controllers.oauth_controller import OAuthLoginView
from src.presentation.controllers.oauth_controller import GoogleAuthView
from src.presentation.controllers.auth_controller import TrustDeviceView
from src.presentation.controllers.mfa_controller import MFASetupView, VerifyMFAView
from src.presentation.controllers.auth_controller import TrustDeviceView

schema_view = get_schema_view(
    openapi.Info(
        title="Auth Service API",
        default_version='v1',
        description="API documentation for Auth Microservice",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


auth_urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordConfirmView.as_view()),

    # MFA
    path("mfa/setup/", MFASetupView.as_view(), name="mfa-setup"),
    path("mfa/verify/", VerifyMFAView.as_view()),
    path("mfa/trust-device/", TrustDeviceView.as_view()),

    # OAuth
    path('oauth/google/', GoogleAuthView.as_view()),

    # Profile
    path("profile/", UserProfileController.as_view()),
    path("profile/update/", UserProfileUpdateController.as_view()),
    path("profile/upload-image/", UserProfileImageUploadController.as_view()),
]



urlpatterns = [
    path('admin/', admin.site.urls),

    # Your custom authentication controllers
    path('api/auth/', include(auth_urlpatterns)),

    # ❌ REMOVE THIS — It breaks your GoogleAuthView endpoint
    # path('api/auth/oauth/', include('social_django.urls', namespace='social')),
]


# Swagger routes
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),

    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    path('redoc/', 
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
