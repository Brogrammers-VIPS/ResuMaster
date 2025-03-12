import requests
import json

# API endpoint and key
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
api_key = ''  # Replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}

def fetch_linkedin_profile(url):
    response = requests.get(api_endpoint,
                            params={'url': url, 'skills': 'include'},
                            headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching LinkedIn profile: {response.status_code}")
        print(response.text)
        return {"Error fetching LinkedIn profile":response.text}

# Main function
if __name__ == "__main__":
    linkedin_profile_url = input("Enter LinkedIn profile URL (e.g., https://www.linkedin.com/in/shivang-rustagi-aa0a8724a/): ").strip()

    profile_data = fetch_linkedin_profile(linkedin_profile_url)

    if profile_data:
        resume_data = {
            "full_name": profile_data.get("full_name", "Unknown Name"),
            "experiences": [],
            "education": [],
            "skills": profile_data.get("skills", [])
        }

        for exp in profile_data.get("experiences", []):
            resume_data["experiences"].append({
                "title": exp.get("title", "Unknown"),
                "company": exp.get("company", "Unknown"),
                "location": exp.get("location", "Unknown"),
                "description": exp.get("description", "No description available"),
                "starts_at": exp.get("starts_at", {}).get("year", "Unknown") if exp.get("starts_at") else "Unknown",
                "ends_at": exp.get("ends_at", {}).get("year", "Present") if exp.get("ends_at") else "Present"
            })

        for edu in profile_data.get("education", []):
            resume_data["education"].append({
                "school": edu.get("school", "Unknown"),
                "degree": edu.get("degree", "Unknown"),
                "field_of_study": edu.get("field_of_study", "Unknown"),
                "starts_at": edu.get("starts_at", {}).get("year", "Unknown") if edu.get("starts_at") else "Unknown",
                "ends_at": edu.get("ends_at", {}).get("year", "Unknown") if edu.get("ends_at") else "Unknown"
            })

        output_file = "resume_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(resume_data, f, indent=4)

        print(json.dumps(resume_data, indent=4))
        print(f"Resume data saved to {output_file}")