import requests
from bs4 import BeautifulSoup

from app.config import settings


def get_html(url, params=None):
    r = requests.get(url=url, headers=settings.HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("span", class_="item")
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("tr", class_="wrap")

    posts = []
    for item in items:
        image = item.find("img", class_="fleft")
        price = item.find("p", class_="price")
        if image:
            image = image.get("src")
        if price:
            price = price.get_text(strip=True)
        posts.append(
            {
                "title": item.find("a", class_="link").get_text(strip=True),
                "price": price,
                "location": item.find("small", class_="breadcrumb").find_next("small", class_="breadcrumb").get_text(strip=True),
                "image": image,
                "link": item.find("a", class_="detailsLink").get("href"),
            }
        )
    return posts


def parse():
    html = get_html(settings.URL)
    if html.status_code == 200:
        posts = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f"Parsing page {page}/{pages_count}...")
            html = get_html(settings.URL, params={"page": page})
            posts.extend(get_content(html.text))
        print(posts)
    else:
        print("Error")


parse()
