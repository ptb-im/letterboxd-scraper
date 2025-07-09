# scrape_letterboxd.py

import requests
from bs4 import BeautifulSoup
import json

USERNAME = "paulietheboss"
URL = f"https://letterboxd.com/{USERNAME}/films/diary/"

def scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    films = []

    for entry in soup.select(".diary-entry-row")[:4]:
        title = entry.select_one(".td-film-details .film-title").text.strip()
        date = entry.select_one(".td-day").text.strip()
        film_url = "https://letterboxd.com" + entry.select_one("a.film-title")["href"]
        films.append({
            "title": title,
            "date": date,
            "url": film_url
        })

    with open("latest_films.json", "w") as f:
        json.dump(films, f, indent=2)

if __name__ == "__main__":
    scrape()
