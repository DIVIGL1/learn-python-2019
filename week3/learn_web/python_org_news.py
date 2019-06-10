import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return (result.text)
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка.")
        return (False)

def get_python_news():
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = BeautifulSoup(html, "html.parser")
        all_news = soup.find("ul", class_="list-recent-posts").findAll("li")
        result_news = []
        for one_news in all_news:
            news_title = one_news.find("a").text
            news_url = one_news.find("a")["href"]
            news_date = one_news.find("time").text
            result_news = result_news + \
                    [{
                        "title": news_title,
                        "url": news_url,
                        "published": news_date
                    }]

        return(result_news)
    else:
        return(False)

