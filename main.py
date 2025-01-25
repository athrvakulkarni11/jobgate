from llm import GroqResponseAnalyzer
import os
import json
import csv
from dotenv import load_dotenv

load_dotenv()

def main():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("Error: Missing GROQ_API_KEY")
        return

    try:
        with open("job_data.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return

    analyzer = GroqResponseAnalyzer(groq_api_key)
    all_jobs = []

    for source_link, content in data.items():
        print(f"Processing: {source_link}")
        jobs = analyzer.extract_jobs(content)
        
        if jobs and isinstance(jobs, list):
            # Filter and format the job entries
            for job in jobs:
                # Create new dict with only required fields
                filtered_job = {
                    "company": job.get("company", "N/A"),
                    "jobrole": job.get("jobrole", "N/A"),
                    "title": job.get("title", "N/A"),
                    "source_link": source_link
                }
                all_jobs.append(filtered_job)
            print(f"Found {len(jobs)} jobs")
        else:
            print("No jobs found in this section")

    # Save to CSV
    if all_jobs:
        with open("jobs.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["company", "jobrole", "title", "source_link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_jobs)
        print(f"Saved {len(all_jobs)} jobs to jobs.csv")
    else:
        print("No jobs found in any sections")

if __name__ == "__main__":
    main()