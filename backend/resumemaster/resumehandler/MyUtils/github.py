import json
import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# LinkedIn API endpoint and key
API_ENDPOINT = 'https://nubela.co/proxycurl/api/v2/linkedin'
API_KEY = ''  # Replace with your actual API key
HEADERS = {'Authorization': 'Bearer ' + API_KEY}

def fetch_linkedin_profile(url):
    """
    Fetch LinkedIn profile data using the Proxycurl API.
    """
    try:
        response = requests.get(API_ENDPOINT,
                                params={'url': url, 'skills': 'include'},
                                headers=HEADERS)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching LinkedIn profile: {response.status_code}")
            print(response.text)
            return {"error": f"Failed to fetch profile: {response.status_code}", "details": response.text}
    except Exception as e:
        print(f"An exception occurred while fetching LinkedIn profile: {e}")
        return {"error": "Exception occurred", "details": str(e)}

def get_linkedin_data(linkedin_profile_url: str) -> dict:
    """
    Process LinkedIn profile data and save it as JSON.
    """
    try:
        # Fetch profile data from the API
        profile_data = fetch_linkedin_profile(linkedin_profile_url)

        if "error" in profile_data:
            print("Error encountered while fetching profile data.")
            return profile_data

        # Parse and structure the resume data
        resume_data = {
            "full_name": profile_data.get("full_name", "Unknown Name"),
            "experiences": [],
            "education": [],
            "skills": profile_data.get("skills", [])
        }

        # Extract work experiences
        for exp in profile_data.get("experiences", []):
            resume_data["experiences"].append({
                "title": exp.get("title", "Unknown"),
                "company": exp.get("company", "Unknown"),
                "location": exp.get("location", "Unknown"),
                "description": exp.get("description", "No description available"),
                "starts_at": exp.get("starts_at", {}).get("year", "Unknown") if exp.get("starts_at") else "Unknown",
                "ends_at": exp.get("ends_at", {}).get("year", "Present") if exp.get("ends_at") else "Present"
            })

        # Extract education details
        for edu in profile_data.get("education", []):
            resume_data["education"].append({
                "school": edu.get("school", "Unknown"),
                "degree": edu.get("degree", "Unknown"),
                "field_of_study": edu.get("field_of_study", "Unknown"),
                "starts_at": edu.get("starts_at", {}).get("year", "Unknown") if edu.get("starts_at") else "Unknown",
                "ends_at": edu.get("ends_at", {}).get("year", "Unknown") if edu.get("ends_at") else "Unknown"
            })

        # Save the structured resume data to a JSON file
        output_file = "resume_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(resume_data, f, indent=4, ensure_ascii=False)

        print(json.dumps(resume_data, indent=4))
        print(f"Resume data saved to {output_file}")
        return resume_data

    except Exception as e:
        print(f"An exception occurred while processing LinkedIn data: {e}")
        return {"error": "Exception occurred", "details": str(e)}

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

def format_experience(experiences):
    story = []
    styles = getSampleStyleSheet()
    for exp in experiences:
        story.append(Paragraph(f"<b>{exp['title']}</b> at {exp['company']} ({exp['location']})", styles['Heading3']))
        story.append(Paragraph(f"Duration: {exp['starts_at']} - {exp['ends_at']}", styles['BodyText']))
        story.append(Paragraph(f"Description: {exp['description']}", styles['BodyText']))
        story.append(Spacer(1, 12))
    return story

def format_education(education):
    story = []
    styles = getSampleStyleSheet()
    for edu in education:
        story.append(Paragraph(f"<b>{edu['school']}</b> ({edu['degree']}, {edu['field_of_study']})", styles['Heading3']))
        story.append(Paragraph(f"Duration: {edu['starts_at']} - {edu['ends_at']}", styles['BodyText']))
        story.append(Spacer(1, 12))
    return story

def format_skills(skills):
    story = []
    styles = getSampleStyleSheet()
    skills_text = ", ".join(skills)
    story.append(Paragraph(f"<b>Skills:</b> {skills_text}", styles['BodyText']))
    story.append(Spacer(1, 12))
    return story

def format_personal_details(name, email, phone, languages, linkedin_url):
    story = []
    styles = getSampleStyleSheet()
    
    # Add name
    story.append(Paragraph(f"<b>{name}</b>", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Add contact details
    contact_details = f"✉️ {email} | 📞 {phone} | 🌐 <link href='{linkedin_url}'>{linkedin_url}</link>"
    story.append(Paragraph(contact_details, styles['BodyText']))
    story.append(Spacer(1, 12))
    
    # Add languages
    languages_text = ", ".join([lang.strip() for lang in languages])
    story.append(Paragraph(f"<b>Languages:</b> {languages_text}", styles['BodyText']))
    story.append(Spacer(1, 12))
    
    return story

def generate_resume_story(name, email, phone, languages, linkedin_url, projects, resume_data):
    styles = getSampleStyleSheet()
    story = []

    # Add personal details
    story.extend(format_personal_details(name, email, phone, languages, linkedin_url))

    # Add experience
    if resume_data["experiences"]:
        story.append(Paragraph("<u>Experience</u>", styles['Heading2']))
        story.extend(format_experience(resume_data["experiences"]))
    else:
        story.append(Paragraph("Experience: No experience data available.", styles['BodyText']))

    # Add education
    if resume_data["education"]:
        story.append(Paragraph("<u>Education</u>", styles['Heading2']))
        story.extend(format_education(resume_data["education"]))
    else:
        story.append(Paragraph("Education: No education data available.", styles['BodyText']))

    # Add skills
    if resume_data["skills"]:
        story.append(Paragraph("<u>Skills</u>", styles['Heading2']))
        story.extend(format_skills(resume_data["skills"]))
    else:
        story.append(Paragraph("Skills: No skills data available.", styles['BodyText']))

    # Add GitHub projects
    story.append(Paragraph("<u>GitHub Projects</u>", styles['Heading2']))
    story.append(Spacer(1, 12))

    for project in projects:
        project_name = Paragraph(f"<b>{project['name']}</b>", styles['Heading3'])
        project_url = Paragraph(f"<link href='{project['url']}'>{project['url']}</link>", styles['BodyText'])
        project_desc = Paragraph(project['description'], styles['BodyText'])
        project_language = Paragraph(f"<b>Language:</b> {project['language']}", styles['BodyText'])
        project_stars = Paragraph(f"<b>⭐ Stars:</b> {project['stars']}", styles['BodyText'])

        story.extend([project_name, project_url, project_desc, project_language, project_stars, Spacer(1, 12)])

    return story

def generate_resume_pdf(name, email, phone, languages, linkedin_url, projects, resume_data, output_pdf):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    story = generate_resume_story(name, email, phone, languages, linkedin_url, projects, resume_data)
    doc.build(story)

if __name__ == "__main__":
    # Prompt user for personal details
    name = input("Enter your full name: ")
    email = input("Enter your email address: ")
    phone = input("Enter your phone number: ")
    languages = input("Enter languages you know (comma-separated): ").split(',')

    # Prompt user for LinkedIn profile URL
    linkedin_profile_url = input("Enter LinkedIn profile URL (e.g., https://www.linkedin.com/in/shivang-rustagi-aa0a8724a/): ").strip()

    # Validate the URL format
    if not linkedin_profile_url.startswith("https://www.linkedin.com/in/"):
        print("Invalid LinkedIn profile URL. Please enter a valid URL.")
    else:
        # Fetch and process LinkedIn data
        resume_data = get_linkedin_data(linkedin_profile_url)

    # Prompt user for GitHub username
    username = input("Enter GitHub username: ")
    projects = fetch_github_projects(username)

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
    generate_resume_pdf(name, email, phone, languages, linkedin_profile_url, selected_projects, resume_data, "resume.pdf")
    print("Resume PDF generated successfully!")