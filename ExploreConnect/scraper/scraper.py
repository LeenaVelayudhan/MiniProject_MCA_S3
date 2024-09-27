from scraper.models import Continent, Country
import requests
from bs4 import BeautifulSoup

def scrape_and_save():
    url = "https://www.lonelyplanet.com/destinations"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        
        for continent_tag in soup.select('a.continent-link'):
            continent_name = continent_tag.text.strip()
            continent_url = "https://www.lonelyplanet.com" + continent_tag['href']
            
            # Save continent to DB
            continent, created = Continent.objects.get_or_create(name=continent_name, url=continent_url)

            # Scrape countries in the continent
            continent_response = requests.get(continent_url, headers=headers)
            continent_soup = BeautifulSoup(continent_response.content, "lxml")
            
            for country_tag in continent_soup.select('a.card__link'):
                country_name = country_tag.text.strip()
                country_url = "https://www.lonelyplanet.com" + country_tag['href']
                country_image = country_tag.find('img')['src'] if country_tag.find('img') else ''
                country_description = country_tag.find('p', class_='description').text.strip() if country_tag.find('p', class_='description') else 'No description available.'

                # Save country to DB
                Country.objects.get_or_create(
                    name=country_name,
                    continent=continent,
                    description=country_description,
                    image=country_image,
                    url=country_url
                )

def scrape_and_save():
    url = "https://www.lonelyplanet.com/destinations"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        
        # Loop through continents
        for continent_tag in soup.select('a.continent-link'):
            continent_name = continent_tag.text.strip()
            continent_url = "https://www.lonelyplanet.com" + continent_tag['href']
            
            # Save continent to DB
            continent, created = Continent.objects.get_or_create(name=continent_name, url=continent_url)

            # Scrape countries in the continent
            continent_response = requests.get(continent_url, headers=headers)
            continent_soup = BeautifulSoup(continent_response.content, "lxml")
            
            for country_tag in continent_soup.select('a.card__link'):
                country_name = country_tag.text.strip()
                country_url = "https://www.lonelyplanet.com" + country_tag['href']
                country_image = country_tag.find('img')['src'] if country_tag.find('img') else ''
                country_description = country_tag.find('p', class_='description').text.strip() if country_tag.find('p', class_='description') else 'No description available.'

                # Save country to DB
                Country.objects.get_or_create(
                    name=country_name,
                    continent=continent,
                    description=country_description,
                    image=country_image,
                    url=country_url
                )
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")