
from django.urls import path
from .views import explain_code

urlpatterns = [
    path("explain/", explain_code, name="explain_code"),
]
