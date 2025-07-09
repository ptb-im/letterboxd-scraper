import requests
from bs4 import BeautifulSoup
import json

USERNAME = "paulietheboss"
URL = f"https://letterboxd.com/{USERNAME}/films/diary/"

def scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Save HTML for debugging
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    films = []
    table = soup.find("table", id="diary-table")
    rows = table.select("tr.diary-entry-row")

    for row in rows[:4]:  # Get only the latest 4
        # Title is in the h2 a tag
        title_tag = row.select_one(".td-film-details h2 a")
        title = title_tag.text.strip() if title_tag else "Unknown"

        # Date watched is in the .td-day column
        date_tag = row.select_one(".td-day a")
        date = date_tag.text.strip() if date_tag else "Unknown"

        # Poster URL is in the <div> with class poster film-poster
        poster_div = row.select_one(".film-poster")
        poster_url = None
        if poster_div and poster_div.has_attr("data-poster-url"):
            poster_path = poster_div["data-poster-url"]
            poster_url = f"https://letterboxd.com{poster_path}"

        films.append({
            "title": title,
            "date": date,
            "poster": poster_url
        })

    with open("latest_films.json", "w", encoding="utf-8") as f:
        json.dump(films, f, indent=2)

if __name__ == "__main__":
    scrape()
