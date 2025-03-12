import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def fetch_github_projects(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []

    repos = response.json()
    project_list = []

    for repo in repos:
        readme_url = f"https://api.github.com/repos/{username}/{repo['name']}/readme"
        readme_response = requests.get(readme_url)

        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = requests.get(readme_data["download_url"]).text
        else:
            readme_content = "No README.md available"

        project = {
            "name": repo["name"],
            "description": readme_content,
            "url": repo["html_url"],
            "language": repo["language"] if repo["language"] else "Not specified",
            "stars": repo["stargazers_count"],
        }
        project_list.append(project)

    return project_list