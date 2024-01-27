from django.shortcuts import render , redirect
from .models import Profile , Message
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm , ProfileForm, SkillsForm , MessageForm
from .utils import paginator_users, search_profile
from .single_yt import *
# Create your views here.

# Notes : working on reviews 

def login_user(request) :
    page = 'login'
    
    # Don't let the login user see the login page and 
    # redirect them to profiles page 
    if request.user.is_authenticated :
        return redirect('profiles')
    
    if request.method == 'POST' : 
        username = request.POST['username'].lower()
        password = request.POST['password']

        try :
            user = User.objects.get(username=username)
        except :
            print("L")
        
        user = authenticate(request , username=username , password=password )
        
        # redirect logined user to profiles page 
        if user is not None :
            login(request , user)
            messages.info(request , "Welcome Back !")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else :
            messages.error(request , message="Whopsie You Did Something Wrong 😳")
        
        
    return render(request , 'users/login-register.html')


def logout_user(request) :
    logout(request)
    messages.info(request , message="Logged out")
    return redirect('login')


def register_user(request) :
    page = 'register'
    form = CustomUserCreationForm()
    
    
    if request.method == "POST" :
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid() :
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request , 'User Account has Been created')
            login(request , user)
            return redirect('edit-account')
        else :
            messages.error(request , "Can't make your account right now please try again !")
        
    
    context = {'page' : page , 'form' : form}
    return render(request , 'users/login-register.html' , context)



def profiles(request) :
    search_result = ''
    
    Profiles , search_result = search_profile(request)
    customRange , Profiles = paginator_users(request , Profiles , 6)
    
    context = {'profiles' : Profiles , 'search_result' : search_result , 'customRange' : customRange }
    return render(request , 'users/profiles.html' , context)


def user_profile(request , pk) :
    user = Profile.objects.get(id=pk)
    topSkill = user.skill_set.exclude(description__exact="")
    otherSkill = user.skill_set.filter(description__exact="")
     
    context ={'user' : user , "topskill" : topSkill , "otherskill" : otherSkill }
    # Check user profile for fixing this page
    return render(request , 'users/user-profile.html' , context)


@login_required(login_url='login')
def user_account(request ) :
    user = request.user.profile
    
    Skill = user.skill_set.all()
   
    
    context = {'profile' : user , "skills" : Skill}
    return render(request , 'users/account.html' , context)


@login_required(login_url="login")
def edit_profile(request) :
    user = request.user.profile
    form = ProfileForm(instance=user)
    
    if request.method == 'POST' :
        form = ProfileForm(request.POST , request.FILES , instance=user)
        if form.is_valid() :
            form.save()
            return redirect('account')
            
        
    context = {'form' : form}
    return render(request , 'users/profile-form.html' , context)


@login_required(login_url="login")
def create_skill(request) :
    profile = request.user.profile 
    form = SkillsForm()
    
    if request.method == 'POST' : 
        form = SkillsForm(request.POST)
        
        if form.is_valid :
            skill = form.save(commit=False)
            skill.owner = profile
            
            skill.save()
            return redirect('account')
    
    context = {"form" : form}
    return render(request , 'users/skill-form.html' , context) 


@login_required(login_url="login")
def edit_skill(request , pk ) : 
    profile = request.user.profile 
    
    user = profile.skill_set.get(id=pk)
    
    form = SkillsForm(instance=user)
    
    if request.method == 'POST' :
        form = SkillsForm(request.POST , instance=user)
        if form.is_valid() : 
            form.save()
            return redirect('account')
        
    context = {"form" : form}
    return render(request , 'users/skill-form.html' , context)


@login_required(login_url="login") 
def delete_skill(request , pk ) : 
    profile = request.user.profile
    
    skill = profile.skill_set.get(id=pk)
    
    if request.method == "POST" :
        skill.delete()
        return redirect('account')
    context = {'object' : skill}
    return render(request , 'users/delete_confirm.html' , context)
   
   
def download(request) :
    search_link=""
    if request.GET.get("search_link") :
        print("Got the link")
        url = request.GET.get('search_link')
        print(url)
        
    else :
        print("Didn't recived the link")
        
    context = {'search_link' : search_link}
    return render(request , 'users/youtube.html' , context)

@login_required(login_url="login") 
def inbox(request) : 
    profile = request.user.profile
    messageRequests = profile.messages.all() 
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequest' : messageRequests , 'unreadCount' : unreadCount }
    return render(request , 'users/inbox.html' , context )


@login_required(login_url="login")
def viewMessage(request , pk): 
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False : 
        message.is_read = True 
        message.save()
    context = {"message" : message}
    return render(request , 'users/message.html' , context)
    

def createMessage(request, pk) :
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try : 
        sender = request.user.profile
    except :
        sender = None 
    
    if request.method == "POST" : 
        form = MessageForm(request.POST)
        if form.is_valid() : 
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender : 
                message.name = sender.name 
                message.email = sender.email
            message.save()
            
            messages.success(request , "Your message has been sent")
            return redirect('user-profile' , pk=recipient.id)
    
    context = {'recipient' : recipient , 'form' : form}
    return render(request , 'users/message_template.html' , context)


def creators(request): 
    context = {}
    return render(request , "users/creators.html", context)