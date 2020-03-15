from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from .models import *
from .forms import *

class MovieListView(ListView):
    model = Movie


class MovieDetailView(DetailView):
    model = Movie


class MovieFormView(FormView):
    template_name = 'movies/movie_form.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_list')

    def form_valid(self, form):
        form.scrape_movie()
        return super().form_valid(form)