from django.db.models import Q 
from .models import project , Tag
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage


def paginator_project(request , projects , result ) :
    
    # paginating and fixing if user enters a page which is not included in the range 
    page = request.GET.get('page')
    paginator = Paginator(projects , result)
    try :
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1 
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page) 
        
    leftindex  = (int(page) - 4 ) 
    rightindex = (int(page) + 5 )
    
    if leftindex < 1 :
        leftindex = 1 
        
    if rightindex > paginator.num_pages :
        rightindex = paginator.num_pages + 1 
        
    customRange = range(leftindex , rightindex) 
    
    return customRange , projects





def project_search(request) :
    search_result = ""
    
    if request.GET.get('search_result') :
        search_result = request.GET.get('search_result') 
    
    tags = Tag.objects.filter(name__icontains=search_result)
    
    projects = project.objects.distinct().filter(Q(title__icontains=search_result) |
                                                 Q(description__icontains=search_result) |
                                                 Q(tags__in=tags) |
                                                 Q(owner__name__icontains=search_result)) 
    
    return projects , search_result