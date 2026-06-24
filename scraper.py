import requests
from bs4 import BeautifulSoup


def fetch_ca_grants():

    url = "https://www.grants.ca.gov/grants/"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        grants = []

        for link in soup.find_all("a", href=True):

            title = link.get_text(strip=True)
            href = link["href"]

            if not title:
                continue

            if "/grants/" not in href:
                continue

            # Skip pagination pages
            if "/page/" in href:
                continue

            if href.startswith("/"):
                href = "https://www.grants.ca.gov" + href

            grants.append({
                "title": title,
                "url": href,
                "source": "California Grants Portal"
            })

        unique = []
        seen = set()

        for g in grants:
            if g["url"] not in seen:
                unique.append(g)
                seen.add(g["url"])

        return unique

    except Exception as e:
        return [{
            "title": f"ERROR: {e}",
            "url": ""
        }]


def fetch_grant_text(url):

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            ["script", "style"]
        ):
            tag.decompose()

        text = soup.get_text(
            " ",
            strip=True
        )

        if "grants.gov" in url:

            print("\n====================")
            print("GRANTS.GOV SAMPLE")
            print(url)
            print("====================")
            print(text[:3000])
            print("====================\n")

        return text

    except Exception as e:

        print(
            "TEXT FETCH ERROR:",
            url,
            e
        )

        return ""