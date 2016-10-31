from django.db import models

# Create your models here.
class urls(models.Model):
    
      short_id=models.SlugField(max_length=6,primary_key=True)
      teamname=models.TextField(max_length=20)
      contestant1=models.TextField(max_length=20)
      contestant2=models.TextField(max_length=20)
      contact=models.TextField(max_length=10)
      pub_date=models.DateTimeField(auto_now=True)

def _str_(self):
      
       return self.teamname