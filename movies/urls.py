from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieFormView.as_view(), name='movie_form'),
    path('movies', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail')
]