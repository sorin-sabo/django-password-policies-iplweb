from django.urls import re_path

from password_policies.views import (
    PasswordChangeDoneView,
    PasswordChangeFormView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetFormView,
)

urlpatterns = [
    re_path(
        route=r"^change/done/$",
        view=PasswordChangeDoneView.as_view(),
        name="password_change_done"
    ),
    re_path(
        route=r"^change/$",
        view=PasswordChangeFormView.as_view(),
        name="password_change"),
    re_path(
        route=r"^reset/$",
        view=PasswordResetFormView.as_view(),
        name="password_reset"
    ),
    re_path(
        route=r"^reset/complete/$",
        view=PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    re_path(
        route=r"^reset/confirm/([0-9A-Za-z_\-]+)/([0-9A-Za-z]{1,13})/([0-9A-Za-z-=_]{1,128})/$",
        view=PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    re_path(
        route=r"^reset/done/$",
        view=PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
]
