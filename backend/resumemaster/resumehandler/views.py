from django.shortcuts import render
from django.http import JsonResponse,HttpRequest
from linkedin_scrapper import *
from github_scrapping import *
def test(request):
    return JsonResponse({"hello":"world"})

def get_projects(request:HttpRequest)-> list:
    if  request.method=='POST':
        return fetch_github_projects(request.POST['username'])

def linkdin_profile(request:HttpRequest)->dict:
    if request.method =='POST':
        return fetch_linkedin_profile(request.POST['url'])