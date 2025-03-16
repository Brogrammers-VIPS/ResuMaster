"""
URL configuration for resumemaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from resumehandler.views import *
urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
    path('get-projects/', GitHubProjectsView.as_view(), name='get-projects'),
    path('build-resume/', ResumeBuilderView.as_view(), name='build-resume'),
    path('recommendation/', Recommendation.as_view(), name='recommendation'),
    path('get-profile-data/',ProfileDataView.as_view(),name='get-profile-data'),
]
