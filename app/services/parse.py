import requests
from bs4 import BeautifulSoup
from requests import Response

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
        location = item.find("small", class_="breadcrumb")
        if image:
            image = image.get("src")
        if price:
            price = price.get_text(strip=True)
        if location:
            location = location.find_next("small", class_="breadcrumb").get_text(strip=True)
        posts.append(
            {
                "title": item.find("a", class_="link").get_text(strip=True),
                "price": price,
                "location": location,
                "image": image,
                "link": item.find("a", class_="detailsLink").get("href"),
            }
        )
    return posts


def replace_gap_on_dash(text: str):
    return text.replace(" ", "-")


def create_params_dict(currency: str = None, p_from: int = 0, p_to: int = 0):
    price_from = "search[filter_float_price:from]"
    price_to = "search[filter_float_price:to]"
    params = dict()
    params["currency"] = currency
    if p_from != 0:
        params[price_from] = p_from
    if p_to != 0:
        params[price_to] = p_to
    return params


def parse(search: str, currency: str = None, p_from: int = 0, p_to: int = 0):
    search = replace_gap_on_dash(search)
    parameters = create_params_dict(currency, p_from, p_to)
    url = settings.URL + f"q-{search}/"
    print(url)
    html = get_html(url)
    if html.status_code == 200:
        posts = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f"Parsing page {page}/{pages_count}...")
            parameters["page"] = page
            html = get_html(url, params=parameters)
            posts.extend(get_content(html.text))
        return posts
    else:
        return Response(status_code=404)
