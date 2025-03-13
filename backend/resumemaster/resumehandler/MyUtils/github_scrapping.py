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

    # Sort repositories by creation date (most recent first)
    sorted_repos = sorted(repos, key=lambda repo: repo["created_at"], reverse=True)

    project_list = []

    for repo in sorted_repos:
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


def summarize_project_description(description):
    if description == "No README.md available":
        return description
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-001")
        response = model.generate_content(f"Summarize this project description in 2 sentences: {description}")
        return response.text.strip()
    except Exception as e:
        print(f"Error with Gemini AI: {e}")
        return description


def generate_resume_story(name:str, projects:list)->list:
    
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(f"{name}'s Resume", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    section_header = Paragraph("GitHub Projects", styles['Heading2'])
    story.append(section_header)
    story.append(Spacer(1, 12))

    for project in projects:
        project_name = Paragraph(f"<b>{project['name']}</b>", styles['Heading3'])
        project_url = Paragraph(f"<link href='{project['url']}'>{project['url']}</link>", styles['BodyText'])
        project_desc = Paragraph(project['description'], styles['BodyText'])
        project_language = Paragraph(f"<b>Language:</b> {project['language']}", styles['BodyText'])
        project_stars = Paragraph(f"<b>⭐ Stars:</b> {project['stars']}", styles['BodyText'])

        story.extend([project_name, project_url, project_desc, project_language, project_stars, Spacer(1, 12)])

    return story


# if __name__ == "__main__":
#     username = input("Enter GitHub username: ")
#     projects = fetch_github_projects(username)

<<<<<<< HEAD:backend/github_scrapping.py
    if not projects:
        print("No repositories found.")
        exit(1)

    # Display repositories with indices
    print("\nRepositories fetched:")
    for i, project in enumerate(projects, start=1):
        print(f"{i}. {project['name']} ({project['language']}, ⭐ {project['stars']})")

    # Prompt user to select repositories
    selected_indices = input("\nEnter the numbers of the repositories you want to include (comma-separated): ")
    selected_indices = [int(idx.strip()) - 1 for idx in selected_indices.split(",") if idx.strip().isdigit()]

    # Filter selected repositories
    selected_projects = [projects[i] for i in selected_indices if 0 <= i < len(projects)]

    if not selected_projects:
        print("No valid repositories selected.")
        exit(1)

    # Summarize descriptions for selected projects
    for project in selected_projects:
        project["description"] = summarize_project_description(project["description"])

    # Generate PDF
    generate_resume_pdf(username, selected_projects, "resume.pdf")
    print("Resume PDF generated successfully!")
=======
#     for project in projects:
#         project["description"] = summarize_project_description(project["description"])

#     generate_resume_story(username, projects, "resume.pdf")
#     print("Resume PDF generated successfully!")
>>>>>>> cfb75c3bafb51196016adeea2cbaab639010b032:backend/resumemaster/resumehandler/MyUtils/github_scrapping.py
