from django.urls import path
from . import views

app_name = 'presignedURL'

urlpatterns = [
    path('aws/presignedURL/', views.PresignedURLView.as_view())
]