import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse

def find_js_urls(base_url):
    """
    Finds JavaScript URLs within a given base URL.

    Args:
        base_url (str): The base URL to scan.

    Returns:
        list: A list of JavaScript URLs found.
    """

    js_urls = []

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all JavaScript URLs
        js_urls = [urljoin(base_url, script['src']) for script in soup.find_all('script', src=True)]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {base_url}: {e}")

    return js_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find JavaScript files in given subdomains.")
    parser.add_argument("-f", "--file", required=True, help="Input file containing subdomains")

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        subdomains = [line.strip() for line in f]

    for subdomain in subdomains:
        base_url = f"https://{subdomain}"  # Assuming HTTPS
        print(f"Scanning {base_url}...")
        js_urls = find_js_urls(base_url)
        if js_urls:
            print("JavaScript files found:")
            for js_url in js_urls:
                print(js_url)
        else:
            print("No JavaScript files found.")
