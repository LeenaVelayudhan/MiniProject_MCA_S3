import requests
from bs4 import BeautifulSoup
import time

def scrape_places():
    base_url = 'https://www.lonelyplanet.com'
    all_results = []

    for page_number in range(2, 5):  # Adjust range as needed
        url = f'{base_url}/places?type=City&sort=DESC&page={page_number}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')

            for article in articles:
                link = article.find('a', class_='text-lg font-bold card-link lg:text-xl')
                if link:
                    destination_name = link.find(text=True, recursive=False).strip()

                    country_tag = link.find('div', class_='text-sm uppercase font-semibold tracking-wide z-10 mt-4 text-black-400 block')
                    country_name = country_tag.text.strip() if country_tag else 'Country not found'

                    href = link.get('href')
                    
                    # Ensure href starts with a '/'
                    if not href.startswith('/'):
                        href = f'/{href}'
                    
                    page_url = f'{base_url}{href}'  # Concatenate base URL and href

                    # Handle image fetching
                    img_tag = article.find('img')
                    image_url = 'No image found'
                    if img_tag and 'srcset' in img_tag.attrs:
                        srcset = img_tag['srcset']
                        image_url = srcset.split(',')[0].split(' ')[0]

                    try:
                        # Fetch description from the destination's page
                        page_response = requests.get(page_url)
                        page_response.raise_for_status()
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')

                        # Get description
                        description_tag = page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg')
                        description = description_tag.text.strip() if description_tag else 'Description not found'

                    except Exception as e:
                        description = f'Error fetching page: {e}'

                    all_results.append({
                        'destination_name': destination_name,
                        'href': href.strip('/'),  # Strip slashes for URL matching
                        'description': description,
                        'image_url': image_url,
                        'country_name': country_name
                    })
        else:
            print(f"Failed to fetch page {page_number}: Status code {response.status_code}")

        # Delay between requests
        time.sleep(1)

    return all_results
