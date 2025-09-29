import pandas as pd
import re
from bs4 import BeautifulSoup
import requests


def extract_state(location_string):
    """Extracts the state abbreviation from a location string.

    Args:
        location_string: The location string (e.g., "Phoenix, AZ, USA" or "US West us-phoenix-1").

    Returns:
        The state abbreviation if found, None otherwise.
    """
    if not location_string:
        return None

    # Try to extract state from the first format (e.g., "Phoenix, AZ, USA")
    match1 = re.search(r',\s*([A-Z]{2})\s*,', location_string)
    if match1:
        return match1.group(1)

    # Try to extract state from the second format (e.g., "US West us-phoenix-1")
    match2 = re.search(r'us-([a-z]+)-', location_string)
    if match2:
        # This format gives city, so we need a mapping from city to state
        # This is a simplified example, a more robust solution might need a dictionary
        city_to_state = {
            'phoenix': 'AZ',
            'ashburn': 'VA',
            'dallas': 'TX',
            # Add more city to state mappings as needed
        }
        city = match2.group(1)
        return city_to_state.get(city.lower())

    return None


def extract_datacenter_locations(html_content):
    """Extracts datacenter location information from HTML content.

    Args:
        html_content: The HTML content of the page.

    Returns:
        A list of location strings.
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    locations = []

    # Look for locations in the first div structure
    for div in soup.find_all('div', class_='text-xs text-gray-500'):
        locations.append(div.get_text(strip=True))

    # Look for locations in the second div structure
    for div in soup.find_all('div', class_='text font-medium hover:text-purple'):
        locations.append(div.get_text(strip=True))

    return locations


def extract_datacenter_data(html_content):
    """Extracts datacenter location and title information from HTML content.

    Args:
        html_content: The HTML content of the page.

    Returns:
        A list of dictionaries, each containing 'location' and 'title'.
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    datacenter_data = []

    # Find all list items which seem to contain each data center's info
    list_items = soup.select('ul > li')

    for item in list_items:
        location = None
        title = None

        # Try to find location in the first div structure
        location_div_1 = item.select_one('div.text-xs.text-gray-500')
        if location_div_1:
            location = location_div_1.get_text(strip=True)

        # Try to find location in the second div structure
        location_div_2 = item.select_one('div.text.font-medium.hover:text-purple')
        if location_div_2:
            location = location_div_2.get_text(strip=True)

        # Try to find the title (inspecting the HTML suggests it might be in an h2 or a strong tag within the list item)
        title_tag_h2 = item.select_one('h2')
        title_tag_strong = item.select_one('strong')

        if title_tag_h2:
            title = title_tag_h2.get_text(strip=True)
        elif title_tag_strong:
            title = title_tag_strong.get_text(strip=True)

        if location or title:  # Only add if at least one piece of information is found
            datacenter_data.append({'location': location, 'title': title})

    return datacenter_data


def fetch_html_content(url):
    """Fetches the HTML content of a given URL.

    Args:
        url: The URL to fetch content from.

    Returns:
        The text content of the response if successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def main():
    all_states = []

    df_states = pd.DataFrame(all_states, columns=['State'])
    print(df_states.head())
    print(f"DataFrame shape: {df_states.shape}")

    base_url = "https://www.datacenters.com/locations/united-states"
    total_pages = 74

    for page_num in range(1, total_pages + 1):
        url = f"{base_url}?page={page_num}"
        print(f"Fetching data from page {page_num}/{total_pages}...")
        html_content = fetch_html_content(url)

        if html_content:
            locations = extract_datacenter_locations(html_content)
            for location in locations:
                state = extract_state(location)
                if state:
                    all_states.append(state)
        else:
            print(f"Could not fetch content from page {page_num}. Skipping.")

    print("Finished collecting data from all pages.")
    print(f"Total states collected: {len(all_states)}")

if __name__ == "__main__":
    main()
