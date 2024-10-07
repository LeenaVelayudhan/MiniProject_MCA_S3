import requests
from bs4 import BeautifulSoup
import time

def scrape_places():
    base_url = 'https://www.lonelyplanet.com'
    all_results = []
    seen_destinations = set()

    for page_number in range(2, 5):  # Adjust range as needed
        url = f'{base_url}/places?type=City&sort=DESC&page={page_number}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')

            for article in articles:
                link = article.find('a', class_='text-lg font-bold card-link lg:text-xl')
                if link:
                    # Extract the destination name
                    destination_name = link.find(text=True, recursive=False).strip()
                    
                    # Extract country name
                    country_tag = article.find('div', class_='text-sm uppercase font-semibold tracking-wide z-10 mt-4 text-black-400 block')
                    country_name = country_tag.text.strip() if country_tag else 'Country not found'

                    # Check for duplicates to prevent adding the same destination multiple times
                    destination_key = (destination_name, country_name)
                    if destination_key not in seen_destinations:
                        seen_destinations.add(destination_key)

                        # Ensure href starts with a '/'
                        href = link.get('href')
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

                            # Get destination description
                            destination_description_tag = page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg')
                            destination_description = destination_description_tag.text.strip() if destination_description_tag else 'Description not found'

                            # Debugging: Print the entire page soup for inspection
                            # print(page_soup.prettify())  # Uncomment to view the full HTML content

                            # Get all relevant paragraphs to find the country description
                            country_description_tags = page_soup.find_all('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg')
                            
                           # Try to find country description, checking more tags if necessary
                            country_description = 'Country description not found'  # Default

                            for tag in country_description_tags:
                                tag_text = tag.text.strip().lower()
                                
                                if country_name.lower() in tag_text and destination_description.lower() not in tag_text:
                                    country_description = tag.text.strip()
                                    break

                            # Fallback approach if country description isn't found directly
                            if country_description == 'Country description not found':
                                for tag in country_description_tags:
                                    if 'climate' in tag_text or 'population' in tag_text or 'tourism' in tag_text:
                                        country_description = tag.text.strip()
                                        break

                        except Exception as e:
                            destination_description = f'Error fetching page: {e}'
                            country_description = 'Error fetching country description'

                        # Append results to the list
                        all_results.append({
                            'destination_name': destination_name,
                            'href': href.strip('/'),  # Strip slashes for URL matching
                            'destination_description': destination_description,
                            'country_description': country_description,
                            'image_url': image_url,
                            'country_name': country_name
                        })
                        

        else:
            print(f"Failed to fetch page {page_number}: Status code {response.status_code}")

        # Delay between requests
        time.sleep(1)

    return all_results



def scrape_best_time_to_visit(place):
    # Construct the URL
    url = f"https://lonelyplanet.com/articles/best-time-to-visit-{place}"
    print("Constructed URL:", url)  # Debugging line

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)

    # Check for HTTP errors
    if response.status_code != 200:
        return f"Failed to retrieve data for {place}: HTTP {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific elements containing the best time information
    best_time_info = soup.find_all('h2')
    info_paragraphs = soup.find_all('p')

    if not best_time_info and not info_paragraphs:
        return f"No best time info found for {place}."

    best_time_text = []
    
    # Aggregate the found text
    for heading in best_time_info:
        best_time_text.append(heading.get_text(strip=True))
        
    for paragraph in info_paragraphs:
        best_time_text.append(paragraph.get_text(strip=True))

    # If no information was collected, inform the user
    if not best_time_text:
        return f"No details available for {place}."

    return "\n\n".join(best_time_text)
