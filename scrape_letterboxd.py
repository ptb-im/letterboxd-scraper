import requests
from bs4 import BeautifulSoup
import json

USERNAME = "paulietheboss"
URL = f"https://letterboxd.com/{USERNAME}/films/diary/"

def scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Write debug HTML so we can inspect what's being scraped
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    table = soup.find("table", id="diary-table")
    rows = table.find_all("tr", class_="diary-entry-row") if table else []

    films = []
    for row in rows[:4]:  # Limit to 4 most recent
        # Title (from <h2> inside .td-film-details)
        title_tag = row.select_one(".td-film-details h2 a")
        title = title_tag.text.strip() if title_tag else "Unknown"

        # Watch date (from .td-day a)
        date_tag = row.select_one(".td-day a")
        date = date_tag.text.strip() if date_tag else "Unknown"

        # Poster image URL (from <img src=...> inside .film-poster)
        poster_img = row.select_one(".film-poster img")
        poster_url = poster_img["src"] if poster_img and poster_img.has_attr("src") else None

        films.append({
            "title": title,
            "date": date,
            "poster": poster_url
        })

    with open("latest_films.json", "w", encoding="utf-8") as f:
        json.dump(films, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape()
