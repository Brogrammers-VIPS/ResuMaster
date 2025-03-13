import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Helper function to format date
def format_date(date_str):
    if not date_str:
        return "Present"
    return date_str 

def fetch_linkedin_profile(url):
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    api = 'BjkQVAiC55Te9t1zEmiFZg'
    headers = {'Authorization': 'Bearer ' + api}
    
    response = requests.get(api_endpoint, params={'url': url}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching LinkedIn profile: {response.status_code}")
        print(response.text)
        return None
    
def fetch_github_projects(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 403:
        print("Error: You have exceeded the GitHub API rate limit. Please try again later.")
        return []

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

# Function to summarize text using Gemini AI
def summarize_text(text):
    if not text or text.strip() == "":
        return "No description available."

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Summarize this in 2 sentences: {text}")
        return response.text.strip()
    except Exception as e:
        print(f"Error with Gemini AI: {e}")
        return text

# Function to generate a resume based on the selected template
def generate_resume_pdf(name, projects, output_pdf, contact_info, work_experience, education, skills, languages):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle('Custom', parent=styles['Normal'], fontSize=10, leading=12)

    story = []

    # Add title
    title = Paragraph(name, styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Add contact information
    contact_info_text = " ".join([f"{icon} {info}" for icon, info in contact_info])
    story.append(Paragraph(contact_info_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # Add work experience section
    story.append(Paragraph("Work Experience", styles['Heading2']))
    if work_experience:
        for exp in work_experience:
            title = exp.get("title", "Unknown Title")
            company = exp.get("company", "Unknown Company")
            location = exp.get("location", "Unknown Location")
            starts_at = format_date(exp.get("starts_at", ""))
            ends_at = format_date(exp.get("ends_at", ""))
            description = exp.get("description", "No description available")

            story.append(Paragraph(f"<b>{title}</b> at {company} ({location})", styles['Heading3']))
            story.append(Paragraph(f"Duration: {starts_at} - {ends_at}", styles['BodyText']))
            story.append(Paragraph(summarize_text(description), custom_style))
            story.append(Spacer(1, 12))
    else:
        story.append(Paragraph("No work experience data available.", styles['BodyText']))

    # Add education section
    story.append(Paragraph("Education", styles['Heading2']))
    if education:
        for edu in education:
            school = edu.get("school", "Unknown School")
            degree = edu.get("degree", "Unknown Degree")
            field_of_study = edu.get("field_of_study", "Unknown Field of Study")
            starts_at = format_date(edu.get("starts_at", ""))
            ends_at = format_date(edu.get("ends_at", ""))

            story.append(Paragraph(f"<b>{school}</b> ({degree}, {field_of_study})", styles['Heading3']))
            story.append(Paragraph(f"Duration: {starts_at} - {ends_at}", styles['BodyText']))
            story.append(Spacer(1, 12))
    else:
        story.append(Paragraph("No education data available.", styles['BodyText']))

    # Add projects section
    story.append(Paragraph("Projects", styles['Heading2']))
    if projects:
        for project in projects:
            project_name = Paragraph(f"<b>{project.get('name', 'Unknown')}</b>", styles['Heading3'])
            project_url = Paragraph(f"<link href='{project.get('url', '')}'>{project.get('url', 'No URL available')}</link>", styles['BodyText'])
            project_desc = Paragraph(summarize_text(project.get('description', '')), custom_style)
            project_language = Paragraph(f"<b>Language:</b> {project.get('language', 'Not specified')}", styles['BodyText'])
            project_stars = Paragraph(f"<b>⭐ Stars:</b> {project.get('stars', 0)}", styles['BodyText'])

            story.extend([project_name, project_url, project_desc, project_language, project_stars, Spacer(1, 12)])
    else:
        story.append(Paragraph("No projects available.", styles['BodyText']))

    # Add skills section
    story.append(Paragraph("Skills", styles['Heading2']))
    if skills:
        skills_text = ", ".join(skills)
        story.append(Paragraph(f"<b>Skills:</b> {skills_text}", styles['BodyText']))
    else:
        story.append(Paragraph("No skills data available.", styles['BodyText']))
    story.append(Spacer(1, 12))

    # Add languages section
    story.append(Paragraph("Languages", styles['Heading2']))
    if languages:
        languages_text = ", ".join(languages) if languages else "No language data available."
        story.append(Paragraph(languages_text, styles['BodyText']))
    else:
        story.append(Paragraph("No languages data available.", styles['BodyText']))
    story.append(Spacer(1, 12))

    # Build the PDF document
    doc.build(story)

if __name__ == "__main__":
    # Step 1: Ask user to select a template
    print("Available templates:")
    print("1. Template 1: Simple and Clean")
    print("2. Template 2: Professional and Highlighted")
    print("3. Template 3: Detailed Resume")
    template_choice = input("Select a template (1, 2, or 3): ").strip()

    template_name = "template_1" if template_choice == "1" else "template_2" if template_choice == "2" else "template_3" if template_choice == "3" else None

    if not template_name:
        print("Invalid template choice. Exiting...")
        exit(1)

    # Step 2: Ask user for LinkedIn profile URL
    linkedin_profile_url = input("Enter LinkedIn profile URL: ")
    linkedin_data = fetch_linkedin_profile(linkedin_profile_url)

    if not linkedin_data:
        print("Failed to fetch LinkedIn profile data. Exiting...")
        exit(1)

    # Extract relevant sections from LinkedIn data
    work_experience = linkedin_data.get("experience", [])
    education = linkedin_data.get("education", [])
    skills = linkedin_data.get("skills", [])

    # Step 3: Ask user for GitHub username
    github_username = input("Enter GitHub username: ")
    projects = fetch_github_projects(github_username)

    if not projects:
        print("No repositories found. Exiting...")
        exit(1)

    # Step 4: Allow user to select specific repositories
    print("\nRepositories fetched:")
    for i, project in enumerate(projects, start=1):
        print(f"{i}. {project.get('name', 'Unknown')} ({project.get('language', 'Not specified')}, ⭐ {project.get('stars', 0)})")

    selected_indices = input("\nEnter the numbers of the repositories you want to include (comma-separated): ")
    selected_indices = [int(idx.strip()) - 1 for idx in selected_indices.split(",") if idx.strip().isdigit()]

    selected_projects = [projects[i] for i in selected_indices if 0 <= i < len(projects)]

    if not selected_projects:
        print("No valid repositories selected. Exiting...")
        exit(1)

    # Step 5: Gather additional user information
    name = input("Enter your full name: ")
    email = input("Enter your email address: ")
    phone = input("Enter your phone number: ")
    languages = input("Enter languages you know (comma-separated): ").split(',')

    contact_info = [
        ("@", email),
        ("📞", phone),
        ("LinkedIn:", linkedin_profile_url)
    ]
    

    # Step 6: Generate the resume
    output_pdf = "resume.pdf"
    import os
    print(f"PDF will be saved at: {os.path.abspath(output_pdf)}")
    generate_resume_pdf(
        template_name,
        name,
        selected_projects,
        output_pdf,
        contact_info,
        work_experience,
        education,
        skills,
        languages
    )
    print(f"Resume PDF generated successfully as '{output_pdf}'!")