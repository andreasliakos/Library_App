from django.urls import path
from .views import (
    Register,
    Login,
    Logout,
    UserTokenRefreshView,
    ResetPasswordRequestView,
    ResetPasswordConfirmView,
    ProtectedAPIView,
)

urlpatterns = [
    path("auth/register/", Register.as_view(), name="register"),
    path("auth/login/", Login.as_view(), name="token_obtain_pair"),
    path("auth/logout/", Logout.as_view(), name="logout"),
    path("auth/token/refresh/", UserTokenRefreshView.as_view(), name="token_refresh"),
    path(
        "password-reset/",
        ResetPasswordRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset-confirm/",
        ResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("protected-endpoint/", ProtectedAPIView.as_view(), name="protected_endpoint"),
]
