from typing import TypedDict
from rest_framework import serializers

# TypedDict for structured return types
class GitHubProject(TypedDict):
    name: str
    language: str
    stars: int
    description: str

class ResumeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    languages = serializers.CharField()
    linkedin_profile_url = serializers.URLField()
    github_username = serializers.CharField(max_length=150)

class GitHubSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
