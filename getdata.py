import requests
import time
import random
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")
id = os.getenv("ID")

job_listing_websites=["glassdoor","indeed","naukri","monster","shine","timesjobs","linkedin"]
def google_search(query,api_key,id,num_results):
    
    url = f"https://www.googleapis.com/customsearch/v1"
    
    params = {
        "q": query,
        "key": api_key,
        "cx": id,
        "num": num_results
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results=response.json()
        return [item['link'] for item in results['items',[]]]
    except requests.exceptions.HTTPError as err:
        print(err)
        return []



results=[]
for website in job_listing_websites:
    query=f"list current jobs as ai engineer at {website}"
    res = google_search(query, api_key, id, 5)
    results.extend(res)    
# results = google_search("list current jobs as ai engineer at Glassdoor", API_KEY, SEARCH_ENGINE_ID, 5)
print(results) 
# url = results[0].split(",")# Replace with the URL of the webpage
# print(url[0])
jsn={
    
}

for res in results:
    response = requests.get(res)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_text = soup.get_text()
# print("data: "+all_text)
    if "job" in all_text.lower():
        print("job found")
        title = soup.find_all('title')
        paragraph = soup.find_all('p')
        # print(title)
        # print(paragraph)
        if title and paragraph:
            jsn[title[0].text]=[p.text for p in paragraph]
        # json[title[0].text]=paragraph[0].text

with open("data.json","w") as file:
    json.dump(jsn,file,indent=4)