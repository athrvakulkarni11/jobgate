import requests
from bs4 import BeautifulSoup
import json
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
@app.get("/get_naukri_jobs")
def get_jobs_list():
    # encoded_job_title = quote(job_title)
    # encoded_location = quote(location)
    response = requests.get(f"https://www.naukri.com/jobs-in-india")
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    all_text = soup.get_text()
    print(all_text)
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
    # import csv
    # with open("jobs.csv", "w", newline="") as f:
    #     writer = csv.DictWriter(f, fieldnames=["title", "jobrole", "location","link"])
    #     writer.writeheader()
    #     writer.writerows(jobs_list)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="8000")