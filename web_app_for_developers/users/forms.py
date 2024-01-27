from django.forms import ModelForm 
from .models import Message, Profile, Skill
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

class CustomUserCreationForm(UserCreationForm) :
    class Meta :
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'username' , 'password1' , 'password2']
        
    def __init__(self , *args , **kwargs) :
        super(CustomUserCreationForm , self).__init__(*args , **kwargs)
        
         
        for name , field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})
            
class ProfileForm(ModelForm) :
    class Meta:
        model = Profile
        fields = ['name' , 'last_name', 'username' , 'location' , 'email' , 'short_intro' , 'bio' , 'profile_img' , 'social_github', 'social_twitter', 'social_linkedin' , 'social_youtube']
        
    def __init__(self , *args , **kwargs) :
        super(ProfileForm , self).__init__(*args , **kwargs)
        
         
        for name , field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})
            

class SkillsForm(ModelForm) :
    class Meta :
        model = Skill
        fields = ['name',  'description']
   
    def __init__(self , *args , **kwargs) :
        super(SkillsForm , self).__init__(*args , **kwargs)
         
        
         
        for name , field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})
            
class MessageForm(ModelForm) :
    class Meta :
        model = Message
        fields = ['name' , 'email' , 'subject' , 'body']
        
    def __init__(self , *args , **kwargs) :
        super(MessageForm , self).__init__(*args , **kwargs)
         
         
         
        for name , field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})