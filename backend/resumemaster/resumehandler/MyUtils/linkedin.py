import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
<<<<<<< HEAD:backend/linkedin.py

=======
from resumehandler.MyUtils.linkedin_scrapper import *
# Function to load JSON data from file
>>>>>>> cfb75c3bafb51196016adeea2cbaab639010b032:backend/resumemaster/resumehandler/MyUtils/linkedin.py
def load_resume_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

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
<<<<<<< HEAD:backend/linkedin.py
def generate_resume(resume_data, output_pdf):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
=======
# Function to generate the full resume
def get_linkdin_story(linkdin_url:str)->list:
    resume_data=get_linkdin_data(linkdin_url)
>>>>>>> cfb75c3bafb51196016adeea2cbaab639010b032:backend/resumemaster/resumehandler/MyUtils/linkedin.py
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<u>Resume for {resume_data['full_name']}</u>", styles['Title']))
    story.append(Spacer(1, 12))

    if resume_data["experiences"]:
        story.append(Paragraph("<u>Experience</u>", styles['Heading2']))
        story.extend(format_experience(resume_data["experiences"]))
    else:
        story.append(Paragraph("Experience: No experience data available.", styles['BodyText']))

    if resume_data["education"]:
        story.append(Paragraph("<u>Education</u>", styles['Heading2']))
        story.extend(format_education(resume_data["education"]))
    else:
        story.append(Paragraph("Education: No education data available.", styles['BodyText']))

    if resume_data["skills"]:
        story.append(Paragraph("<u>Skills</u>", styles['Heading2']))
        story.extend(format_skills(resume_data["skills"]))
    else:
        story.append(Paragraph("Skills: No skills data available.", styles['BodyText']))

<<<<<<< HEAD:backend/linkedin.py
    doc.build(story)

if __name__ == "__main__":
    resume_data = load_resume_data("resume_data.json")

output_pdf = "resume.pdf"
generate_resume(resume_data, output_pdf)
print(f"Resume saved to {output_pdf}")
=======
# Build the PDF
    return story

# Main function
# if __name__ == "__main__":
# # Load resume data from JSON file
#     resume_data = load_resume_data("resume_data.json")

# # Generate the resume in PDF format
# output_pdf = "resume.pdf"
# get_linkdin_story(resume_data, output_pdf)
# print(f"Resume saved to {output_pdf}")
>>>>>>> cfb75c3bafb51196016adeea2cbaab639010b032:backend/resumemaster/resumehandler/MyUtils/linkedin.py
