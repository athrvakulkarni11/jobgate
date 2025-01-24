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
                    Include company, title, description, and source. Structure as: 
                    [{{"company": "...", "title": "...", "description": "...", "source": "..."}}]
                    Content:\n{combined_content}"""
                }],
                model="llama3-8b-8192",
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error processing content: {str(e)}")
            return []
