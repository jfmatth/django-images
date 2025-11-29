from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="images-index"),
    path('upload/', views.UploadView.as_view(), name='images-upload'),
]