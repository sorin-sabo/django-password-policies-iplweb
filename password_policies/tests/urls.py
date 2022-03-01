from django.urls import include, re_path

try:
    from django.conf.urls import patterns
except ImportError:
    patterns = False

from password_policies.tests.views import TestHomeView, TestLoggedOutMixinView


urlpatterns = [
    re_path(r"^password/", include("password_policies.urls")),
    re_path(r"^$", TestHomeView.as_view(), name="home"),
    re_path(r"^fubar/", TestLoggedOutMixinView.as_view(), name="loggedoutmixin"),
]

if patterns:
    urlpatterns = patterns("", *urlpatterns)  # noqa
