import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django import forms
from movies.models import Movie, Review, Person, Genre

def scrape_movie_page(url):
    page = requests.get(url)
    if (page.status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")

        # Scrape movie name
        movie_name = soup.find('h1', class_="pvi-product-title")

        # Scrape average note
        note = soup.find('span', class_="pvi-scrating-value").text

        # Scrape release date
        result = soup.find_all('li', class_='pvi-productDetails-item')
        date_str = result[3].find('time')['datetime']
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        m, m_created = Movie.objects.get_or_create(
            name=movie_name['title'],
            average_note=float(note),
            release_date=date
        )

        if m_created == True:
            # Scrape genre
            result = soup.find_all('span', itemprop="genre")
            for item in result:
                movie_genre = item.text
                g, g_created = Genre.objects.get_or_create(genre=movie_genre)
                if g_created:
                    g.save()
                m.genres.add(g)

            # Scrape directors
            result = soup.find_all('span', itemprop="director")
            for item in result:
                director = item.find('span', itemprop="name").text
                d, d_created = Person.objects.get_or_create(name=director, role=Person.Role.Director)
                if d_created:
                    d.save()
                m.persons.add(d)


            # Access to the detail page
            page = requests.get(url + "/details")
            if (page.status_code == 200):
                soup = BeautifulSoup(page.content, "html.parser")

                # Scrape main actors
                result = soup.find_all("div", class_="ecot-contact")
                for item in result:
                    if (item.find('span', class_='ecot-contact-role') != None):
                        actor = item.find('span', class_='ecot-contact-label').text
                        a, a_created = Person.objects.get_or_create(name=actor, role=Person.Role.Actor)
                        if a_created:
                            a.save()
                        m.persons.add(a)

                # Scrape other actors
                result = soup.find("table", class_="pde-data").find_all("td", class_="pde-data-label")
                for item in result:
                    actor = item.find("a")
                    if (actor != None):
                        actor = actor.text
                        a, a_created = Person.objects.get_or_create(name=actor, role=Person.Role.Actor)
                        if a_created:
                            a.save()
                        m.persons.add(a)


            # # Issue:    Review pages seem dynamically loaded so we can't access the data we want with BeautifulSoup.
            # #           Need to run the scripts before getting the HTML somehow.          

            # Access positive reviews page
            page = requests.get(url + "/critiques#page-1/filter-positive")
            if (page.status_code == 200):
                soup = BeautifulSoup(page.content, "html.parser")

                # Scrape positive reviews
                result = soup.find_all("article", class_="ere-review")
                count = 0
                for item in result:
                    rev_note = int(item.find("span", class_="elrua-useraction-inner").text)
                    if (rev_note > 5):
                        rev_title = item.find("h3").text
                        # Accessing the page with the full review
                        review_link = item.find("a", "ere-review-anchor")['href']
                        review_page = requests.get("https://www.senscritique.com" + review_link)
                        if (review_page.status_code == 200):
                            # Scraping author and full review
                            review_soup = BeautifulSoup(review_page.content, "html.parser")
                            rev_author = review_soup.find("span", itemprop="author").find("span", itemprop="name").text
                            review = review_soup.find("div", class_="rvi-review-content").text
                            r, r_created = Review.objects.get_or_create(
                                title=rev_title,
                                author=rev_author,
                                note=rev_note,
                                text=review,
                                movie=m
                            )
                            if r_created:
                                r.save()
                        count += 1
                    if (count >= 2):
                        break

            # Access negative reviews page
            page = requests.get(url + "/critiques#page-1/filter-negative")
            if (page.status_code == 200):
                soup = BeautifulSoup(page.content, "html.parser")
                
                # Scrape negative reviews
                result = soup.find_all("article", class_="ere-review")
                count = 0
                for item in result:
                    rev_note = int(item.find("span", class_="elrua-useraction-inner").text)
                    if (rev_note < 5):
                        rev_title = item.find("h3").text
                        # Accessing the page with the full review
                        review_link = item.find("a", "ere-review-anchor")['href']
                        review_page = requests.get("https://www.senscritique.com" + review_link)
                        if (review_page.status_code == 200):
                            # Scraping author and full review
                            review_soup = BeautifulSoup(review_page.content, "html.parser")
                            rev_author = review_soup.find("span", itemprop="author").find("span", itemprop="name").text
                            review = review_soup.find("div", class_="rvi-review-content").text
                            r, r_created = Review.objects.get_or_create(
                                title=rev_title,
                                author=rev_author,
                                note=rev_note,
                                text=review,
                                movie=m
                            )
                            if r_created:
                                r.save()
                        count += 1
                    if (count >= 2):
                        break


class MovieForm(forms.Form):
    movie_url = forms.URLField(label='SensCritique movie url ')

    def scrape_movie(self):
        url = self.cleaned_data['movie_url']
        scrape_movie_page(url)
