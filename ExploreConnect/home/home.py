import requests
from bs4 import BeautifulSoup
import time

def scrape_places():
    base_url = 'https://www.lonelyplanet.com/places?type=City&sort=DESC&page='
    all_results = []

    for page_number in range(2, 5):  # You can dynamically fetch the number of pages instead of hardcoding
        url = f'{base_url}{page_number}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')

            for article in articles:
                link = article.find('a', class_='text-lg font-bold card-link lg:text-xl')

                if link:
                    direct_text = link.find(text=True, recursive=False).strip()
                    href = link.get('href')

                    # Handle image fetching
                    img_tag = article.find('img')
                    image_url = 'No image found'
                    if img_tag and 'srcset' in img_tag.attrs:
                        srcset = img_tag['srcset']
                        image_url = srcset.split(',')[0].split(' ')[0]

                    # Fetch individual page for description
                    page_url = 'https://www.lonelyplanet.com' + href
                    try:
                        page_response = requests.get(page_url)
                        page_response.raise_for_status()  # Will raise an exception for non-200 status codes
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        description_tag = page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg')
                        description = description_tag.text.strip() if description_tag else 'Description not found'
                    except Exception as e:
                        description = f'Error fetching page: {e}'

                    all_results.append({
                        'text': direct_text,
                        'href': href,
                        'description': description,
                        'image_url': image_url
                    })

        else:
            print(f"Failed to fetch page {page_number}: Status code {response.status_code}")

        # Add a short delay to avoid overwhelming the server
        time.sleep(1)  # Adjust the delay as needed

    return all_results
