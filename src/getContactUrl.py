import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from time import sleep
import tls_client


# URL to fetch HTML content from
def available_urls(url):
    session = tls_client.Session(

        client_identifier="chrome112",

        random_tls_extension_order=True

    )
    
    session.headers.update(
        {
            "scheme": "https",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
    )

    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    html_content = str(soup.find_all())
    pattern = rf"{url}[\w\-\./?=&]+"

    urls = re.findall(pattern, html_content)
    unique_urls = set(urls)
    unique_urls.add(url)

    keywords = ["contact", "contact_us", "about"]
    facebook_keyword = "facebook"
    facebook_url = ""

    for index_url in re.findall(r'href="([^"]+)"', html_content):
  
        complete_url = urljoin(url, index_url)
        if any(keyword in complete_url for keyword in keywords):
            unique_urls.add(complete_url)
        if facebook_keyword in complete_url:
            facebook_url = complete_url

    filtered_urls = [
        url for url in unique_urls
        if not re.search(r"\.[a-zA-Z0-9]+$", url) and any(keyword in url for keyword in keywords)
    ]
    filtered_urls.append(url)
    print(filtered_urls)
    return filtered_urls, facebook_url


# print(available_urls("https://www.acejasper.com/"))

