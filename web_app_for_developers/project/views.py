from django.shortcuts import render , redirect
from .forms import ProjectForm , ReviewForm
from .models import project 
from django.contrib.auth.decorators import login_required
from .utils import project_search , paginator_project

# Create your views here.
def projects(request) :
    search_result = ""
    
    
    projects , search_result = project_search(request)
    customRange , projects = paginator_project(request , projects , 6)
        
    
    context = {'project' : projects , 'search_result' : search_result , "customRange" : customRange }  
    return render(request , 'project/project.html' , context)

def projectPK(request , pk) :
    projectObj = project.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method == "POST" :
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.Project = projectObj
        review.owner = request.user.profile
        review.save()
        
        projectObj.getVoteCount
        
        redirect('projectPK' , pk=projectObj.id)
         
    context = {"Key" : projectObj , "form" : form}
    return render(request , "project/singleproject.html" , context) 

@login_required(login_url="login")
def create_project(request) :
    
    profile = request.user.profile
    
    form = ProjectForm()
    
    if request.method == 'POST' : 

        form = ProjectForm(request.POST , request.FILES)
        
        if form.is_valid :
            project = form.save(commit=False)
            project.owner = profile
            
            project.save()
            return redirect('projects')
            
    context = {'form' : form }
    return render(request , "project/project_form.html" , context)

@login_required(login_url="login")
def update_project(request , pk) :
    
    profile = request.user.profile
    
    # projectObj = project.objects.get(id=pk)
    
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)
    if request.method == 'POST' : 
        print(request.POST)
        form = ProjectForm(request.POST , request.FILES, instance=projectObj )
        if form.is_valid :
            form.save()
            return redirect('projects')
            
    context = {'form' : form }
    return render(request , "project/project_form.html" , context)

@login_required(login_url="login")
def delete_project(request , pk) : 
    
    profile = request.user.profile
    
    # projectObj = project.objects.get(id=pk)
    
    projectObj = profile.project_set.get(id=pk)
    if request.method == "POST" :
        projectObj.delete()
        return redirect('projects')
    context = {'object' : projectObj}
    return render(request , 'project/delete_confirm.html' , context)