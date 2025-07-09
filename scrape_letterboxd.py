import requests
from bs4 import BeautifulSoup
import json

USERNAME = "paulietheboss"
URL = f"https://letterboxd.com/{USERNAME}/films/diary/"

def scrape():
    response = requests.get(URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    films = []

    entries = soup.select("ul.diary-table tbody tr")  # safer selector

    for entry in entries[:4]:
        title_el = entry.select_one("td.td-film-details a.film-title")
        date_el = entry.select_one("td.td-day")

        if not title_el or not date_el:
            print("⚠️ Skipping entry: missing title or date")
            continue

        title = title_el.text.strip()
        date = date_el.text.strip()
        film_url = "https://letterboxd.com" + title_el.get("href", "")

        films.append({
            "title": title,
            "date": date,
            "url": film_url
        })

    with open("latest_films.json", "w", encoding="utf-8") as f:
        json.dump(films, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    scrape()
