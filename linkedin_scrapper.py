import requests
from bs4 import BeautifulSoup
import re
from fastapi import FastAPI
from urllib.parse import quote

app = FastAPI()

@app.get("/get_linkedin_jobs")
def get_jobs_list(job_title:str,location:str="india"):
    encoded_job_title = quote(job_title)
    encoded_location = quote(location)
    response = requests.get(f"https://www.linkedin.com/jobs/search/?keywords={encoded_job_title}&location={encoded_location}")
    soup = BeautifulSoup(response.text, 'html.parser')
    all_text = soup.get_text()
    all_link_tags = soup.find_all('a', class_='base-card__full-link')

    job_links = []
    for tag in all_link_tags:
        link = tag.get('href')
        if link:
            job_links.append(link)
    jobs_list = []
    print(job_links)
    for res in job_links:
        response = requests.get(res)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text()
    # print("data: "+all_text)
        if "linkedin" in all_text.lower():
            print("job found")
            title = soup.find_all('title')
            # print(title)
            # print(paragraph)
            if title :
                # jsn[res]=[title[0].text]

                text = title[0].text

                # Use regex to parse components
                pattern = r"""
                    (.*?)\s+hiring\s+    # Capture title (text before "hiring")
                    (.*?)\s+in\s+        # Capture job role (text after "hiring" and before "in")
                    (.*?)\s*\|\s*        # Capture location (text after "in" and before "|")
                """


                match = re.search(pattern, text, re.VERBOSE)

                if match:
                    title = match.group(1).strip()    # "Software Engineer"
                    jobrole = match.group(2)          # "SDE3" (or None if missing)
                    location = match.group(3).strip() # "Bengaluru, Karnataka, India"
                    jobs_list.append({
                        "title": title,
                        "jobrole": jobrole,
                        "location": location,
                        "link":res
                    })
                    print(f"Title: {title}")
                    print(f"Job Role: {jobrole}")
                    print(f"Location: {location}")
                else:
                    print("No match found")
                        # json[title[0].text]=paragraph[0].text

    return jobs_list
@app.get("/get_jobzmall_jobs")
def get_jobs_list():
    try:
        # Use a proper headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Verify the actual URL for job listings
        response = requests.get("https://www.jobzmall.com/jobs", headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        
        
        # More robust method to find job links
        job_links = soup.find_all('a', href=True, class_=re.compile(r'job-link|base-card__full-link'))
        
        jobs_list = []
        for link in job_links:
            job_url = link['href']
            
            # Fetch individual job page
            job_response = requests.get(job_url, headers=headers)
            job_soup = BeautifulSoup(job_response.text, 'html.parser')
            
            # More flexible job details extraction
            job_details = {
                'title': job_soup.find(['h1', 'title'], class_=re.compile(r'job-title')).text.strip() if job_soup.find(['h1', 'title'], class_=re.compile(r'job-title')) else 'N/A',
                'company': job_soup.find(['div', 'span'], class_=re.compile(r'company-name')).text.strip() if job_soup.find(['div', 'span'], class_=re.compile(r'company-name')) else 'N/A',
                'location': job_soup.find(['div', 'span'], class_=re.compile(r'job-location')).text.strip() if job_soup.find(['div', 'span'], class_=re.compile(r'job-location')) else 'N/A',
                'link': job_url
            }
            
            jobs_list.append(job_details)
        
        return jobs_list
    
    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return []