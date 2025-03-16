from typing import Dict, List, Any
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .MyUtils import github
from .serializers import ResumeSerializer, GitHubSerializer,Skillset

class TestView(APIView):
    def get(self, request: Request) -> Response:
        return Response({"hello": "world"}, status=status.HTTP_200_OK)

class GitHubProjectsView(APIView):
    def post(self, request: Request) -> Response:
        serializer: GitHubSerializer = GitHubSerializer(data=request.data)
        if serializer.is_valid():
            username: str = serializer.validated_data['username']
            projects: List[Dict[str, Any]] = github.fetch_github_projects(username)
            return Response({"projects": projects}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeBuilderView(APIView):
    def post(self, request: Request) -> Response | FileResponse:
        serializer: ResumeSerializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            data: Dict[str, Any] = serializer.validated_data
            output_pdf: str = "resume.pdf"

            # Validate LinkedIn URL
            linkedin_profile_url: str = data['linkedin_profile_url']
            if not linkedin_profile_url.startswith("https://www.linkedin.com/in/"):
                return Response({"error": "Invalid LinkedIn profile URL"}, status=status.HTTP_400_BAD_REQUEST)

            resume_data: Dict[str, Any] = github.get_linkedin_data(linkedin_profile_url)
            selected_projects: List[Dict[str, Any]] = data['projects']
            for project in selected_projects:
                project["description"] = github.summarize_project_description(project["description"])
            
            template_id: int = data['template_id']
            # Generate Resume
            github.generate_resume_pdf(
                data['name'], data['email'], data['phone'], data['languages'],
                linkedin_profile_url, selected_projects,template_id, resume_data, output_pdf
            )

            try:
                document = open(output_pdf, 'rb')
                return FileResponse(document, content_type='application/pdf')
            except FileNotFoundError:
                return Response({"error": "Resume generation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Recommendation(APIView):
    def post(self, request: Request) -> Response:
        serializer : Skillset = Skillset(data=request.data)
        if serializer.is_valid():
            skills: str = serializer.validated_data['skills']
            result = github.recommendation(skills)

            return Response({"recommended_jobs":result}, status=status.HTTP_200_OK)
        

class ProfileDataView(APIView):
    def post(self, request) -> Response:
        """
        Fetch LinkedIn profile data and summarize GitHub project descriptions.
        """
        linkedin_url: str = request.data.get("linkedin_url", "").strip()
        github_projects: List[Dict[str, Any]] = request.data.get("github_projects", [])

        print(linkedin_url)
        if not linkedin_url.startswith("https://www.linkedin.com/in/"):
            return Response({"error": "Invalid LinkedIn profile URL"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch LinkedIn data
        linkedin_data: Dict[str, Any] = github.get_linkedin_data(linkedin_url)

        print(linkedin_data)
        # Summarize GitHub project descriptions
        summarized_projects: List[Dict[str, Any]] = []
        for project in github_projects:
            summarized_projects.append({
                "name": project["name"],
                "description": github.summarize_project_description(project["description"]),
                "url": project["url"],
                "language": project["language"],
                "stars": project["stars"],
            })

        # Prepare response
        response_data = {
            "full_name": linkedin_data.get("full_name", "Unknown Name"),
            "education": linkedin_data.get("education", []),
            "experience": linkedin_data.get("experiences", []),
            "skills": linkedin_data.get("skills", []),
            "projects": summarized_projects,
        }

        return Response(response_data, status=status.HTTP_200_OK)
