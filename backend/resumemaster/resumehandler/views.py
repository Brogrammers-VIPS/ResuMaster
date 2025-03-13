from django.shortcuts import render
from django.http import JsonResponse,HttpRequest,FileResponse,HttpResponseNotFound
from resumehandler.MyUtils import github_scrapping,linkedin
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

def test(request):
    return JsonResponse({"hello":"world"})

def get_projects(request:HttpRequest)-> list:
    if  request.method=='POST':
        return github_scrapping.fetch_github_projects(request.POST['username'])

def build_resume(request:HttpRequest):
    if request.method=="POST":
        data=request.POST
        output_pdf="resume.pdf"
        doc = SimpleDocTemplate(output_pdf, pagesize=letter)
        projects=data['projects']
        for project in projects:
            project["description"] = github_scrapping.summarize_project_description(project["description"])
        resume_story=github_scrapping.generate_resume_story(data['username'],projects)
        linkdin_story=linkedin.get_linkdin_story(data['linkdin_url'])

        doc.build(resume_story.extend(linkdin_story))

        try:
            document=open(output_pdf,'rb')
            return FileResponse(document)
        except FileNotFoundError:
            return HttpResponseNotFound("Error occured")

