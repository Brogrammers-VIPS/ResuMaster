from typing import Dict, List, Any
from django.http import FileResponse, HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .MyUtils import github_scrapping, github
from .serializers import ResumeSerializer, GitHubSerializer

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
