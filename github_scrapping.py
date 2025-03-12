import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to fetch GitHub projects
def fetch_github_projects(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []

    repos = response.json()
    project_list = []

    for repo in repos:
        project = {
            "name": repo["name"],
            "description": repo["description"] if repo["description"] else "No description available",
            "url": repo["html_url"],
            "language": repo["language"] if repo["language"] else "Not specified",
            "stars": repo["stargazers_count"],
        }
        project_list.append(project)

    return project_list