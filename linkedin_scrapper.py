import requests
from bs4 import BeautifulSoup
import re
from fastapi import FastAPI
from urllib.parse import quote
import uvicorn

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

@app.get("/get_indeed_jobs")
def get_indeed_jobs(job_title: str, location: str = "india"):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        encoded_job_title = quote(job_title)
        encoded_location = quote(location)
        url = f"https://www.indeed.com/jobs?q={encoded_job_title}&l={encoded_location}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        jobs_list = []
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        for card in job_cards:
            title = card.find('h2', class_='jobTitle')
            company = card.find('span', class_='companyName')
            location = card.find('div', class_='companyLocation')
            job_link = card.find('a', class_='jcs-JobTitle')
            
            if title and company and location and job_link:
                jobs_list.append({
                    'title': title.get_text().strip(),
                    'company': company.get_text().strip(),
                    'location': location.get_text().strip(),
                    'link': 'https://www.indeed.com' + job_link.get('href', '')
                })
        
        return jobs_list
    except requests.RequestException as e:
        print(f"Error fetching Indeed jobs: {e}")
        return []

@app.get("/get_glassdoor_jobs")
def get_glassdoor_jobs(job_title: str, location: str = "india"):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        encoded_job_title = quote(job_title)
        encoded_location = quote(location)
        url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={encoded_job_title}&locT=C&locId={encoded_location}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        jobs_list = []
        job_listings = soup.find_all('li', class_='react-job-listing')
        
        for job in job_listings:
            title = job.find('a', class_='jobLink')
            company = job.find('div', class_='emp-name')
            location = job.find('span', class_='loc')
            job_link = job.find('a', class_='jobLink')
            
            if title and company and location and job_link:
                jobs_list.append({
                    'title': title.get_text().strip(),
                    'company': company.get_text().strip(),
                    'location': location.get_text().strip(),
                    'link': 'https://www.glassdoor.com' + job_link.get('href', '')
                })
        
        return jobs_list
    except requests.RequestException as e:
        print(f"Error fetching Glassdoor jobs: {e}")
        return []

if __name__ == "__main__":
    uvicorn.run("linkedin_scrapper:app", host="0.0.0.0", port=8000)    