from django import forms
from movies.models import Movie, Review, Person, Genre
from movies.scripts.scraper import scrape_movie_page

class MovieForm(forms.Form):
    movie_url = forms.URLField(label='SensCritique movie url ')

    def scrape_movie(self):
        url = self.cleaned_data['movie_url']
        scrape_movie_page(url)
