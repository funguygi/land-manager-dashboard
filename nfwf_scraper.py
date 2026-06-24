import requests
from bs4 import BeautifulSoup


def fetch_nfwf_grants():

    url = "https://www.nfwf.org/programs"

    try:

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        grants = []

        for link in soup.find_all("a", href=True):

            title = link.get_text(strip=True)
            title = title.replace("Image", "").strip()
            href = link["href"]

            if len(title) < 5:
                continue

            if "/programs/" not in href:
                continue

            if href.startswith("/"):
                href = "https://www.nfwf.org" + href

            grants.append({
                "title": title,
                "url": href,
                "source": "NFWF",
                "agency": "National Fish and Wildlife Foundation"
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
            "title": f"NFWF ERROR: {e}",
            "url": "",
            "source": "NFWF"
        }]