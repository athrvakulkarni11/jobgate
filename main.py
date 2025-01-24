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
        with open("data.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return

    analyzer = GroqResponseAnalyzer(groq_api_key)
    all_jobs = []

    for title, content in data.items():
        print(f"Processing: {title}")
        jobs = analyzer.extract_jobs(content)
        if jobs and isinstance(jobs, list):
            all_jobs.extend(jobs)
            print(f"Found {len(jobs)} jobs")
        else:
            print("No jobs found in this section")

    # Save to CSV
    if all_jobs:
        with open("jobs.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["company", "title", "description", "source"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_jobs)
        print(f"Saved {len(all_jobs)} jobs to jobs.csv")
    else:
        print("No jobs found in any sections")

if __name__ == "__main__":
    main()
    
    