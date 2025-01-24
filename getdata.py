import requests
import time
import random
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
idx = os.getenv("SEARCH_ENGINE_ID")

job_listing_websites = ["glassdoor", "indeed", "naukri", "monster", "shine", "timesjobs", "linkedin"]

def google_search(query, api_key, idx, num_results):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": idx,
        "num": num_results
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        return [item['link'] for item in results.get('items', [])]
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

results = []
for website in job_listing_websites:
    query = f"list current jobs as AI engineer at {website}"
    res = google_search(query, api_key, idx, 5)
    results.extend(res)
    time.sleep(random.uniform(1, 3))  # Add a delay to avoid being flagged as a bot

print(f"Found {len(results)} results")

jsn = {}
counter = 0

for res in results:
    try:
        response = requests.get(res, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text()
        if "job" in all_text.lower():
            print(f"Job found at {res}")
            title = soup.find('title')
            paragraphs = soup.find_all('p')
            if title and paragraphs:
                jsn[f"{counter + 1}: {title.text.strip()}"] = [p.text.strip() for p in paragraphs]
                counter += 1
        time.sleep(random.uniform(2, 5))  # Throttle scraping requests
    except Exception as e:
        print(f"Error scraping {res}: {e}")

with open("data.json", "w") as file:
    json.dump(jsn, file, indent=4)

# print(f"Data saved to data.json with {len(jsn)} entries.")
 