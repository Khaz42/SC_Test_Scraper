import requests
from bs4 import BeautifulSoup

def scrape_movie_page(url):
    page = requests.get(url)
    if (page.status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")

        # Scrape average note
        result = soup.find('span', class_="pvi-scrating-value")
        print("Average Note :", float(result.text))

        # Scrape directors
        result = soup.find_all('span', itemprop="director")
        for item in result:
            director = item.find('span', itemprop="name").text
            print("Director :", director)

        # Scrape genre
        result = soup.find_all('span', itemprop="genre")
        for item in result:
            genre = item.text
            print("Genre :", genre)

        # Scrape release date
        result = soup.find_all('li', class_='pvi-productDetails-item')
        date = result[3].find('time')['datetime']
        print("Release date :", date)

    # Access to the detail page
    page = requests.get(url + "/details")
    if (page.status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")

        # Scrape main actors
        result = soup.find_all("div", class_="ecot-contact")
        for item in result:
            if (item.find('span', class_='ecot-contact-role') != None):
                actor = item.find('span', class_='ecot-contact-label').text
                print("Main Actor :", actor)

        # Scrape other actors
        result = soup.find("table", class_="pde-data").find_all("td", class_="pde-data-label")
        for item in result:
            actor = item.find("a")
            if (actor != None):
                actor = actor.text
                print("Other Actor :", actor)


    # Issue:    Review pages seem dynamically loaded so we can't access the data we want with BeautifulSoup.
    #           Need to run the scripts before getting the HTML somehow.          

    # Access positive reviews page
    page = requests.get(url + "/critiques#page-1/filter-positive")
    if (page.status_code == 200):
        soup = BeautifulSoup(page.content, "html.parser")

        # Scrape positive reviews
        result = soup.find_all("article", class_="ere-review")
        count = 0
        for item in result:
            note = int(item.find("span", class_="elrua-useraction-inner").text)
            if (note > 5):
                title = item.find("h3").text
                # Accessing the page with the full review
                review_link = item.find("a", "ere-review-anchor")['href']
                review_page = requests.get("https://www.senscritique.com" + review_link)
                if (review_page.status_code == 200):
                    # Scraping author and full review
                    review_soup = BeautifulSoup(review_page.content, "html.parser")
                    author = review_soup.find("span", itemprop="author").find("span", itemprop="name").text
                    review = review_soup.find("div", class_="rvi-review-content").text
                    print("Author : " + author, "| Title : " + title, "| Note : " + str(note))
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
            note = int(item.find("span", class_="elrua-useraction-inner").text)
            # print(note)
            if (note < 5):
                title = item.find("h3").text
                # Accessing the page with the full review
                review_link = item.find("a", "ere-review-anchor")['href']
                review_page = requests.get("https://www.senscritique.com" + review_link)
                if (review_page.status_code == 200):
                    # Scraping author and full review
                    review_soup = BeautifulSoup(review_page.content, "html.parser")
                    author = review_soup.find("span", itemprop="author").find("span", itemprop="name").text
                    review = review_soup.find("div", class_="rvi-review-content").text
                    print("Author : " + author, "| Title : " + title, "| Note : " + str(note))
                count += 1
            if (count >= 2):
                break


if __name__ == "__main__":
    # scrape_movie_page("https://www.senscritique.com/film/Matrix/382239")
    scrape_movie_page("https://www.senscritique.com/film/Fight_Club/363185")