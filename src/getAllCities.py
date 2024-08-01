import requests
from bs4 import BeautifulSoup

async def get_all_cities(state):
    # URL for the list of counties in Texas
    url = "https://en.wikipedia.org/wiki/List_of_counties_in_" + state

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table element that contains the list of counties
    table = soup.find("table", {"class": "wikitable"})

    # Extract the county names from the table
    counties = []
    for row in table.find_all("tr")[1:]:
        county_name = row.find_all("td")[1].text.strip()
        counties.append(county_name)
        
    return counties


print(get_all_cities("Arizona"))

