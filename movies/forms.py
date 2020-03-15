from django import forms

class MovieForm(forms.Form):
    movie_url = forms.URLField(label='SensCritique movie url ')

    def scrape_movie(self):
        url = self.cleaned_data['movie_url']
        