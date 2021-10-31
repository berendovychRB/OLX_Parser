import requests
from bs4 import BeautifulSoup

URL = "https://www.olx.ua/uk/list/q-mazda/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "accept": "*/*",
}


def get_html(url, params=None):
    r = requests.get(url=url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("tr", class_="wrap")

    posts = []
    for item in items:
        image = item.find("img", class_="fleft")
        if image:
            image = image.get("src")
        else:
            image = "----"
        posts.append(
            {
                "title": item.find("a", class_="link").get_text(strip=True),
                "price": item.find("p", class_="price").get_text(strip=True),
                "location": item.find("small", class_="breadcrumb").find_next("small", class_="breadcrumb").get_text(strip=True),
                "image": image,
                "link": item.find("a", class_="detailsLink").get("href"),
            }
        )
    for post in posts:
        print(post)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("Error")


parse()
