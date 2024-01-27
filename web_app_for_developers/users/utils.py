from .models import Profile , Skill
from django.db.models import Q
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

def search_profile(request) :
    search_result = ''
    
    if request.GET.get('search_result') :
        search_result = request.GET.get('search_result')
        
    skill = Skill.objects.filter(name__icontains=search_result)    
    
    Profiles = Profile.objects.distinct().filter(Q(name__icontains=search_result) |
                                                 Q(username__icontains=search_result) |
                                                 Q(skill__in=skill))
    
    return Profiles , search_result 


def paginator_users(request , profiles , result ) :
    
    # paginating and fixing if user enters a page which is not included in the range 
    page = request.GET.get('page')
    paginator = Paginator(profiles , result)
    try :
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1 
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page) 
        
    leftindex  = (int(page) - 4 ) 
    rightindex = (int(page) + 5 )
    
    if leftindex < 1 :
        leftindex = 1 
        
    if rightindex > paginator.num_pages :
        rightindex = paginator.num_pages + 1 
        
    customRange = range(leftindex , rightindex) 
    
    return customRange , profiles