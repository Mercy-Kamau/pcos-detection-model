from django.db import models

# Create your models here.
# models.py
class uploadImage(models.Model):
    name = models.CharField(max_length=50, default=None)
    image = models.ImageField(upload_to='user/uploadImage', default=None)
    
    def _str_(self):
        return self.name
        

all_instances = uploadImage.objects.all()