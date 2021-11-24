from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_view, name='index'),
    path('results/', views.result_view, name='results'),
    path('results/download/', views.download_files, name='download'),
    path('oups/', views.secret, name='secret'),
]