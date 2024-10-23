import requests
from bs4 import BeautifulSoup
import time
import os
import django
import traceback

# Set up Django settings module to match your project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExploreConnect.settings')  # Use the actual name of your settings module
django.setup()



def fetch_soup(url):
    """Fetch the content of the URL and return a BeautifulSoup object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_region_details(region_url):
    """Extract details from the region page."""
    page_soup = fetch_soup(region_url)
    if page_soup is None:
        return 'Region page not found'

    description = 'Region description not found'
    description_tags = page_soup.find_all('p')

    for tag in description_tags:
        if region_url.split('/')[-1].replace('-', ' ').lower() in tag.text.strip().lower():
            description = tag.text.strip()
            break

    return description

def extract_country_details(country_url):
    """Extract details from the country page."""
    page_soup = fetch_soup(country_url)
    if page_soup is None:
        return 'Country page not found'

    description = 'Country description not found'
    description_tags = page_soup.find_all('p')

    for tag in description_tags:
        if country_url.split('/')[-1].replace('-', ' ').lower() in tag.text.strip().lower():
            description = tag.text.strip()
            break

    return description

def extract_continent_details(continent_name):
    """Extract details from the continent page."""
    continent_url = f'https://www.lonelyplanet.com/{continent_name.lower()}'
    page_soup = fetch_soup(continent_url)
    
    if page_soup is None:
        return 'Continent page not found', 'No description found'

    continent_header = page_soup.find('h1', class_='lg:inline text-3xl lg:text-6xl text-blue font-semibold')
    continent_description_tag = page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg')

    continent_name = continent_header.text.strip() if continent_header else 'Continent name not found'
    continent_description = continent_description_tag.text.strip() if continent_description_tag else 'Description not found'

    return continent_name, continent_description

def extract_best_time_to_visit(destination_url):
    """Extract 'best time to visit' details from the destination's best time page."""
    destination_name = destination_url.split('/')[-1]
    best_time_url = f'https://www.lonelyplanet.com/articles/best-time-to-visit-{destination_name}'
    
    page_soup = fetch_soup(best_time_url)
    if page_soup is None:
        return {
            'best_time_title': 'Best time to visit details not found',
            'header_image_url': 'No header image found',
            'intropara': 'Intro paragraph not found',
            'sections': []
        }

    title_tag = page_soup.find('h1', class_='text-4xl md:text-5xl font-display leading-tight font-light max-w-5xl mx-auto text-center my-24', attrs={'data-testid': 'page-heading'})
    best_time_title = title_tag.text.strip() if title_tag else 'Title not found'

    intropara_tag = page_soup.find('p', class_='text-md my-6 text-black-400')
    intropara = intropara_tag.text.strip() if intropara_tag else 'Intro paragraph not found'

    header_image_tag = page_soup.find('div', class_='lg:container lg:px-0')
    header_image_url = 'No header image found'
    if header_image_tag:
        img_tag = header_image_tag.find('img')
        if img_tag and 'src' in img_tag.attrs:
            header_image_url = img_tag['src']

    best_time_details = []
    h2_tags = page_soup.find_all('h2', class_='text-black mt-16 mb-6 article-h2')

    for h2 in h2_tags:
        section = {'title': h2.text.strip(), 'paragraphs': [], 'figures': []}
        current_element = h2.find_next_sibling()
        while current_element and current_element.name != 'h2':
            if current_element.name == 'p':
                section['paragraphs'].append(current_element.text.strip())
            elif current_element.name == 'figure':
                fig_image = current_element.find('img')
                figcaption = current_element.find('figcaption')
                section['figures'].append({
                    'image': fig_image['src'] if fig_image else None,
                    'alt': fig_image['alt'] if fig_image else None,
                    'caption': figcaption.text.strip() if figcaption else None
                })
            current_element = current_element.find_next_sibling()
        best_time_details.append(section)

    return {
        'best_time_title': best_time_title,
        'header_image_url': header_image_url,
        'intropara': intropara,
        'sections': best_time_details
    }

def extract_attractions(destination_url):
    """Extract attractions from the destination page."""
    page_soup = fetch_soup(destination_url)

    if page_soup is None:
        return 'Attractions page not found', []

    attractions_list = []
    attraction_cards = page_soup.find_all('li', class_='col-span-1 md:col-span-3 lg:col-span-3')

    for card in attraction_cards:
        img_tag = card.find('img')
        img_src = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'No image found'

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

        location_tag = card.find('p', class_='text-sm font-semibold uppercase !mt-2')
        location = location_tag.text.strip() if location_tag else 'No location found'

        description_tag = card.find('p', class_='relative line-clamp-3')
        description = description_tag.text.strip() if description_tag else 'No description found'

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
            'Region not found',
            'Country not found', 
            'Continent not found', 
            'No image found',  
            []  
        )

    destination_description = page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg').text.strip() if page_soup.find('p', class_='max-w-2xl min-h-[90px] my-6 leading-loose text-black-400 text-sm lg:text-lg') else 'Description not found'

    breadcrumb_nav = page_soup.find('nav', {'aria-label': 'Breadcrumbs'})
    region_name, country_name, continent_name = 'Region not found', 'Country not found', 'Continent not found'
    country_url, region_url, continent_url = None, None, None

    if breadcrumb_nav:
        breadcrumb_items = breadcrumb_nav.find_all('li')
        if len(breadcrumb_items) >= 3:
            region_link = breadcrumb_items[0].find('a')
            country_link = breadcrumb_items[1].find('a')
            continent_link = breadcrumb_items[2].find('a')

            if region_link:
                region_name = region_link.get_text(strip=True)
                region_url = region_link.get('href')
                region_url = region_url if region_url.startswith('http') else f"{base_url}{region_url}"
            if country_link:
                country_name = country_link.get_text(strip=True)
                country_url = country_link.get('href')
                country_url = country_url if country_url.startswith('http') else f"{base_url}{country_url}"

            if continent_link:
                continent_name = continent_link.get_text(strip=True)
                continent_url = continent_link.get('href')
                continent_url = continent_url if continent_url.startswith('http') else f"{base_url}{continent_url}"

    img_tag = page_soup.find('img', class_='w-full h-full object-cover')
    destination_image = img_tag['src'] if img_tag else 'No image found'

    return (
        destination_description, 
        region_name, region_url, 
        country_name, country_url, 
        continent_name, continent_url, 
        destination_image
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
                    destination_name = link.find(text=True, recursive=False).strip()
                    country_tag = article.find('div', class_='text-sm uppercase font-semibold tracking-wide z-10 mt-4 text-black-400 block')
                    country_name = country_tag.text.strip() if country_tag else 'Country not found'

                    # Check for duplicates
                    destination_key = (destination_name, country_name)
                    if destination_key not in seen_destinations:
                        seen_destinations.add(destination_key)

                        href = link.get('href')
                        if not href.startswith('/'):
                            href = f'/{href}'

                        page_url = f'{base_url}{href}' 

                        try:
                            # Fetch description from the destination's page
                            destination_description, region_name, region_url, country_name,  country_url, continent_name, continent_url, destination_image = extract_destination_details(page_url, base_url)
                            # Fetch country details if a valid country URL is found
                            region_description = 'Region not found'
                            if region_url:
                                print(f"Fetching region details from: {region_url}")
                                region_description = extract_region_details(region_url)
                            country_description = 'Country not found'
                            if country_url:
                                print(f"Fetching country details from: {country_url}")
                                country_description = extract_country_details(country_url)
                            # Fetch continent details using the continent name
                            continent_description = 'Continent not found'
                            if continent_name and continent_name != 'Continent not found':
                                print(f"Fetching continent details from: {continent_url}")
                                continent_description, continent_info = extract_continent_details(continent_name)

                            # Append results to the list
                            all_results.append({
                                'destination_name': destination_name,
                                'href': href.strip('/'),  # Strip slashes for URL matching
                                'destination_description': destination_description,
                                'region_name':region_name,
                                'region_description':region_description,
                                'country_description': country_description,
                                'continent_name': continent_name,
                                'continent_description': continent_info,
                                'image_url': destination_image,  # Include the destination image URL
                                'country_name': country_name,
                                # 'best_time_to_visit': {
                                #     'title': best_time_details['best_time_title'],
                                #     'header_image': best_time_details['header_image_url'],
                                #     'intropara': best_time_details['intropara'],
                                #     'sections': best_time_details['sections']
                                # },  # Include structured best time to visit details
                                # 'attractions': attractions_list  # Include attractions
                            })
                            #Save destination
                            destination = Destination.objects.create(
                                destination_name=destination_name,
                                href=href.strip('/'),
                                destination_description=destination_description,
                                region_name=region_name,
                                region_description=region_description,
                                country_name=country_name,
                                country_description=country_description,
                                continent_name=continent_name,
                                continent_description=continent_description,
                                image_url=destination_image
                            )
                        #     # Save best time to visit (one-to-one relationship)
                        #     BestTimeToVisit.objects.create(
                        #         destination=destination,
                        #         title=best_time_details['best_time_title'],
                        #         header_image=best_time_details['header_image_url'],
                        #         intropara=best_time_details['intropara'],
                        #         sections=best_time_details['sections']
                        #     )

                        #     # Save attractions (many-to-one relationship)
                        #     for attraction in attractions:
                        #         Attraction.objects.create(
                        #             destination=destination,
                        #             name=attraction['attraction_name'],
                        #             description=attraction['description']
                        #         )

                        #     print(f"Saved {destination_name} to the database.")

                        except Exception as e:
                            print(f"Error processing {destination_name}: {e}")

        else:
            print(f"Failed to fetch page: {page_number} Status code {response.status_code}")
            
        # Delay between requests
        time.sleep(1)

    return "Scraping complete!"

                  
