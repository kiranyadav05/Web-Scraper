import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL to scrape
BASE_URL = "http://quotes.toscrape.com"

# Function to fetch HTML content
def fetch_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to parse HTML and extract quotes, authors, and tags
def parse_html(html):
    data = []
    soup = BeautifulSoup(html, "html.parser")
    
    # Find all quote containers
    quotes = soup.find_all("div", class_="quote")
    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)  # Extract quote text
        author = quote.find("small", class_="author").get_text(strip=True)  # Extract author name
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]  # Extract tags
        
        data.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })
    return data

# Function to scrape all pages
def scrape_all_pages(base_url):
    all_data = []
    page = 1
    while True:
        url = f"{base_url}/page/{page}/"
        print(f"Scraping: {url}")
        html_content = fetch_html(url)
        
        if not html_content:
            print("No more pages or failed to retrieve page.")
            break
        
        data = parse_html(html_content)
        if not data:  # Stop if no data found
            print("No data found on this page. Stopping.")
            break
        
        all_data.extend(data)
        page += 1
    return all_data

# Function to save data to CSV
def save_to_csv(data, filename="quotes_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main script
if __name__ == "__main__":
    print("Starting scraper...")
    all_quotes = scrape_all_pages(BASE_URL)
    
    if all_quotes:
        print(f"Total quotes scraped: {len(all_quotes)}")
        save_to_csv(all_quotes)
    else:
        print("No quotes were scraped.")
