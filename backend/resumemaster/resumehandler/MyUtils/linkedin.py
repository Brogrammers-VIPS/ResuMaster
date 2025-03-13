import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
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
def generate_resume(resume_data, output_pdf):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
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

    doc.build(story)

if __name__ == "__main__":
    resume_data = load_resume_data("resume_data.json")

output_pdf = "resume.pdf"
generate_resume(resume_data, output_pdf)
print(f"Resume saved to {output_pdf}")
