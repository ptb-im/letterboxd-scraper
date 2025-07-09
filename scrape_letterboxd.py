import requests
from bs4 import BeautifulSoup
import json

USERNAME = "paulietheboss"
URL = f"https://letterboxd.com/{USERNAME}/films/diary/"

def scrape():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    # Save raw HTML for debugging purposes
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    films = []

    # Select diary entries rows
    entries = soup.select("table#diary-table tr.diary-entry-row")

    for entry in entries[:4]:  # Get last 4 entries
        # Updated selector for title: nested inside td.td-film-details > div.body > header > span > h2.name > a (no class)
        title_el = entry.select_one("td.td-film-details div.body header.inline-production-masthead span h2.name a")

        # Date selector: day number link inside td.td-day.diary-day.center a
        date_el = entry.select_one("td.td-day.diary-day.center a")

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
