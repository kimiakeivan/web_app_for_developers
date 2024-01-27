from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class project(models.Model):
    owner = models.ForeignKey(Profile , null=True , blank=True , on_delete=models.SET_NULL) 
    
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    demo_link = models.CharField(max_length=2000 , null=True , blank=True)
    src_link = models.CharField(max_length=2000 , null=True , blank=True)
    tags = models.ManyToManyField('Tag' , blank=True)
    vote_total = models.IntegerField(default=0 , null=True , blank=True)
    vote_ratio = models.IntegerField(default=0 , null=True , blank=True)
    
    fearured_img = models.ImageField(null=True , blank=True , default="default.jpg")

    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.title 
        
    class Meta:
        ordering = ['-vote_ratio' , '-vote_total' , 'title'] # Remove - at the first will make it oposite
    
    @property
    def reviewers(self) :
        quaryset = self.review_set.all().values_list("owner__id" , flat=True)
        
    
    @property
    def getVoteCount(self) :
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        
        ratio = (upVotes / totalVotes) * 100 
        
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        
       
        
        self.save()
        
        
class review(models.Model) :
    VOTE_TYPE = (
        ('up' , 'up vote'),
        ('down' , 'down vote'),
    )
    owner = models.ForeignKey(Profile , on_delete=models.CASCADE , null=True  )
    Project = models.ForeignKey( project ,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)
    body = models.TextField(blank=True , null=True)
    value = models.CharField(max_length=200 , choices=VOTE_TYPE)
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Meta :
        unique_together = [['owner' , 'Project']]
    
    def __str__(self) :
        return self.value
    
    
class Tag(models.Model) :
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key=True , editable=False)
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.name
     