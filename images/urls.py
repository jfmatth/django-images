from django.urls import path

from . import views
from images.views import ImageStreamView
from .views import health_check

urlpatterns = [
    path('', views.IndexView.as_view(), name="images-index"),
    path('upload/', views.UploadView.as_view(), name='images-upload'),
    path("images/<int:pk>/", ImageStreamView.as_view(), name="image-stream"),
    path("healthz/", health_check),
]
