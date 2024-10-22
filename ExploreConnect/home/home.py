import requests
from bs4 import BeautifulSoup
import time
import os
import django

# Set up Django settings module to match your project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExploreConnect.settings')  # Use the actual name of your settings module
django.setup()

from home.models import Destination, BestTimeToVisit, Attraction  # Replace 'myapp' with the name of your Django app

def fetch_soup(url):
    """Fetch the content of the URL and return a BeautifulSoup object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_country_details(country_url):
    """Extract details from the country page."""
    page_soup = fetch_soup(country_url)
    if page_soup is None:
        return 'Country page not found'

    # Attempt to find the first relevant paragraph that contains the country name
    description = 'Country description not found'
    description_tags = page_soup.find_all('p')

    for tag in description_tags:
        if country_url.split('/')[-1].replace('-', ' ').lower() in tag.text.strip().lower():
            description = tag.text.strip()
            break  # Stop after finding the first relevant description

    return description

def extract_continent_details(continent_name):
    """Extract details from the continent page."""
    # Construct the continent URL based on the continent name
    continent_url = f'https://www.lonelyplanet.com/{continent_name.lower()}'
    page_soup = fetch_soup(continent_url)
    
    if page_soup is None:
        return 'Continent page not found', 'No description found'

    # Extract the continent header and description
    continent_header = page_soup.find('h1', class_='lg:inline text-3xl lg:text-6xl text-blue font-semibold')
    continent_description_tag = page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg')

    continent_name = continent_header.text.strip() if continent_header else 'Continent name not found'
    continent_description = continent_description_tag.text.strip() if continent_description_tag else 'Description not found'

    return continent_name, continent_description

def extract_best_time_to_visit(destination_url):
    """Extract 'best time to visit' details from the destination's best time page."""
    # Extract the destination name from the URL and construct the 'best time to visit' URL
    destination_name = destination_url.split('/')[-1]
    best_time_url = f'https://www.lonelyplanet.com/articles/best-time-to-visit-{destination_name}'
    
    # Fetch and parse the HTML content from the constructed URL
    page_soup = fetch_soup(best_time_url)
    if page_soup is None:
        return {
            'best_time_title': 'Best time to visit details not found',
            'header_image_url': 'No header image found',
            'intropara': 'Intro paragraph not found',
            'sections': []
        }

    # Extract the title from the h1 tag
    title_tag = page_soup.find('h1', class_='text-4xl md:text-5xl font-display leading-tight font-light max-w-5xl mx-auto text-center my-24', attrs={'data-testid': 'page-heading'})
    best_time_title = title_tag.text.strip() if title_tag else 'Title not found'

    # Extract the intro paragraph
    intropara_tag = page_soup.find('p', class_='text-md my-6 text-black-400')
    intropara = intropara_tag.text.strip() if intropara_tag else 'Intro paragraph not found'

    # Extract the header image
    header_image_tag = page_soup.find('div', class_='lg:container lg:px-0')
    header_image_url = 'No header image found'
    if header_image_tag:
        img_tag = header_image_tag.find('img')
        if img_tag and 'src' in img_tag.attrs:
            header_image_url = img_tag['src']

    # List to store section details (best time details)
    best_time_details = []

    # Extract all h2 tags which represent section titles
    h2_tags = page_soup.find_all('h2', class_='text-black mt-16 mb-6 article-h2')

    # Loop through all the h2 elements and extract their associated content
    for h2 in h2_tags:
        section = {'title': h2.text.strip(), 'paragraphs': [], 'figures': []}

        # Get the next sibling and continue until another h2 tag is found
        current_element = h2.find_next_sibling()
        while current_element and current_element.name != 'h2':
            # If it's a paragraph, add it to the section's paragraphs list
            if current_element.name == 'p':
                section['paragraphs'].append(current_element.text.strip())
            # If it's a figure, extract the image and figcaption
            elif current_element.name == 'figure':
                fig_image = current_element.find('img')
                figcaption = current_element.find('figcaption')
                section['figures'].append({
                    'image': fig_image['src'] if fig_image else None,
                    'alt': fig_image['alt'] if fig_image else None,
                    'caption': figcaption.text.strip() if figcaption else None
                })
            # Move to the next sibling
            current_element = current_element.find_next_sibling()
        
        # Add the section to the best_time_details list
        best_time_details.append(section)

    return {
        'best_time_title': best_time_title,
        'header_image_url': header_image_url,
        'intropara': intropara,
        'sections': best_time_details  # Include the list of section details
    }


def extract_attractions(destination_url):
    """Extract attractions from the destination page."""
    attractions_url = f"{destination_url}"
    page_soup = fetch_soup(attractions_url)

    if page_soup is None:
        return 'Attractions page not found', []

    # List to store attractions
    attractions_list = []

    # Find all the attraction cards
    attraction_cards = page_soup.find_all('li', class_='col-span-1 md:col-span-3 lg:col-span-3')

    for card in attraction_cards:
        # Extract the image from the <img> tag in the <article>
        img_tag = card.find('img')
        img_src = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'No image found'

        # Extract the attraction name from the <a> tag inside <p>
        attraction_link_tag = card.find('a', class_='card-link line-clamp-2 w-[80%] md:w-90')
        
        if attraction_link_tag:
            attraction_name_tag = attraction_link_tag.find('span', class_='heading-05 font-semibold')
            attraction_name = attraction_name_tag.text.strip() if attraction_name_tag else 'No name available'
            attraction_href = attraction_link_tag['href'] if attraction_link_tag.has_attr('href') else 'No link available'
            if attraction_href.startswith('/'):
                attraction_href = f"https://www.lonelyplanet.com{attraction_href}"
        else:
            attraction_name = 'None'
            attraction_href = 'None'
        # Extract the location from the <p> tag with class 'text-sm font-semibold uppercase !mt-2'
        location_tag = card.find('p', class_='text-sm font-semibold uppercase !mt-2')
        location = location_tag.text.strip() if location_tag else 'No location found'

        # Extract the description from the <p> tag with class 'relative line-clamp-3'
        description_tag = card.find('p', class_='relative line-clamp-3')
        description = description_tag.text.strip() if description_tag else 'No description found'

        # Append the extracted data to the list
        attractions_list.append({
            'attraction_name': attraction_name,
            'attraction_link': attraction_href,
            'location': location,
            'image': img_src,
            'description': description
        })

    return attractions_list
def extract_destination_details(destination_url, base_url):
    """Extract details from the destination page."""
    page_soup = fetch_soup(destination_url)
    if page_soup is None:
        return (
            'Description not found', 
            'Country not found', 
            'Continent not found', 
            
            'No image found',  # Placeholder for image
            []  # Attractions list
        )

    # Get destination description
    description_tag = page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg')
    destination_description = description_tag.text.strip() if description_tag else 'Description not found'

    # Get breadcrumb navigation for country and continent
    breadcrumb_nav = page_soup.find('nav', {'aria-label': 'Breadcrumbs'})
    country_url = None  # Default value
    continent_name = 'Continent not found'
    
    if breadcrumb_nav:
        breadcrumb_items = breadcrumb_nav.find_all('li')
        if len(breadcrumb_items) >= 2:
            country_link = breadcrumb_items[0].find('a')  # First item is the country
            continent_name = breadcrumb_items[1].get_text(strip=True)  # Second item is the continent
            if country_link:
                country_name = country_link.get_text(strip=True)
                country_url = country_link.get('href')
                # Ensure country URL is absolute
                country_url = country_url if country_url.startswith('http') else f"{base_url}{country_url}"
            else:
                country_name = 'Country not found'
        else:
            country_name = 'Country not found'
    else:
        country_name = 'Country not found'

    # Get destination image
    image_tag = page_soup.find('img')  # Adjust this if needed to find the correct image
    image_url = 'No image found'
    if image_tag and 'srcset' in image_tag.attrs:
        srcset = image_tag['srcset']
        image_url = srcset.split(',')[0].split(' ')[0]

    attractions = extract_attractions(destination_url)

    return (
        destination_description,
        country_name,
        continent_name,
        country_url,
        image_url,  # Return the image URL
        attractions
    )

def scrape_places():
    base_url = 'https://www.lonelyplanet.com'
    all_results = []
    seen_destinations = set()

    for page_number in range(1, 2):  # Adjust range as needed
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

                        try:
                            # Fetch description from the destination's page
                            destination_description, country_name, continent_name, country_url, destination_image, attractions = extract_destination_details(page_url, base_url)

                            attractions_list = extract_attractions(page_url)
                            # Fetch best time to visit details
                            best_time_details = extract_best_time_to_visit(page_url)

                            # Fetch country details if a valid country URL is found
                            country_description = 'Country not found'
                            if country_url:
                                print(f"Fetching country details from: {country_url}")
                                country_description = extract_country_details(country_url)

                            # Fetch continent details using the continent name
                            continent_description = 'Continent not found'
                            if continent_name and continent_name != 'Continent not found':
                                print(f"Fetching continent details from: {continent_name}")
                                continent_description, continent_info = extract_continent_details(continent_name)

                            # Append results to the list
                            all_results.append({
                                'destination_name': destination_name,
                                'href': href.strip('/'),  # Strip slashes for URL matching
                                'destination_description': destination_description,
                                'country_description': country_description,
                                'continent_name': continent_name,
                                'continent_description': continent_info,
                                'image_url': destination_image,  # Include the destination image URL
                                'country_name': country_name,
                                'best_time_to_visit': {
                                    'title': best_time_details['best_time_title'],
                                    'header_image': best_time_details['header_image_url'],
                                    'intropara': best_time_details['intropara'],
                                    'sections': best_time_details['sections']
                                },  # Include structured best time to visit details
                                'attractions': attractions_list  # Include attractions
                            })
                        # Save destination
                            destination = Destination.objects.create(
                                destination_name=destination_name,
                                href=href.strip('/'),
                                destination_description=destination_description,
                                country_name=country_name,
                                country_description=country_description,
                                continent_name=continent_name,
                                continent_description=continent_description,
                                image_url=destination_image
                            )

                            # Save best time to visit (one-to-one relationship)
                            BestTimeToVisit.objects.create(
                                destination=destination,
                                title=best_time_details['best_time_title'],
                                header_image=best_time_details['header_image_url'],
                                intropara=best_time_details['intropara'],
                                sections=best_time_details['sections']
                            )

                            # Save attractions (many-to-one relationship)
                            for attraction in attractions:
                                Attraction.objects.create(
                                    destination=destination,
                                    name=attraction['attraction_name'],
                                    description=attraction['description']
                                )

                            print(f"Saved {destination_name} to the database.")

                        except Exception as e:
                            print(f"Error processing {destination_name}: {e}")

        else:
            print(f"Failed to fetch page: {page_number} Status code {response.status_code}")
            
        # Delay between requests
        time.sleep(1)

    return "Scraping complete!"
                            
