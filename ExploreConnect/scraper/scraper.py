# scraper.py
import requests

def fetch_lonely_planet_html():
    url = 'https://www.lonelyplanet.com/destinations'
    
    try:
        # Fetch the page content using requests
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the raw HTML of the page
            return response.text  # Return the HTML content as a string
        else:
            return f"Failed to retrieve the page. Status code: {response.status_code}"
    
    except Exception as e:
        return f"Error occurred: {e}"
