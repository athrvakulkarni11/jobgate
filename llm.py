import os
import json
import csv
from groq import Groq

class GroqResponseAnalyzer:
    def __init__(self, groq_api_key):
        self.client = Groq(api_key=groq_api_key)
    
    def extract_jobs(self, content):
        """Extract job data from content using LLM"""
        try:
            filtered_content = [c for c in content if c.strip()]
            combined_content = "\n".join(filtered_content)[:3000]
            
            response = self.client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"""Analyze this content and extract job opportunities in JSON format. 
                    Include company name, jobrole, title, and source_link. Structure as: 
                    [{{"company": "...", "title": "...", "jobrole": "...", "source_link": "..."}}]
                    Content:\n{combined_content}"""
                }],
                model="llama3-8b-8192",
                response_format={"type": "json_object"}
            )
            
            extracted_data = json.loads(response.choices[0].message.content)
            
            # If the API returns a dictionary, convert it to a list
            if isinstance(extracted_data, dict):
                extracted_data = [extracted_data]
            
            return extracted_data
        except Exception as e:
            print(f"Error processing content: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    # Your input data (keys = source_links, values = job listings)
    input_data = {
        "https://www.linkedin.com/jobs/view/software-engineer-i-at-nike-4129314029": [
            "Nike hiring Software Engineer I in Beaverton, OR | LinkedIn"
        ],
        # ... other entries
    }

    # Initialize Groq analyzer
    analyzer = GroqResponseAnalyzer(groq_api_key=os.getenv("GROQ_API_KEY"))
    
    # Process all job listings
    final_output = []
    for source_link, job_listings in input_data.items():
        extracted_jobs = analyzer.extract_jobs(job_listings)
        
        # Add source_link to each extracted job
        for job in extracted_jobs:
            job["source_link"] = source_link
            final_output.append({
                "company": job.get("company", ""),
                "jobrole": job.get("jobrole", ""),
                "title": job.get("title", ""),
                "source_link": source_link
            })
    
    # Save to JSON
    with open("jobs.json", "w") as f:
        json.dump(final_output, f, indent=2)
    
    # Save to CSV
    with open("jobs.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["company", "jobrole", "title", "source_link"])
        writer.writeheader()
        writer.writerows(final_output)