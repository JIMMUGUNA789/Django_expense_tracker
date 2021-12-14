from django.db import models

# Create your models here.
from datetime import date
from django.db import models
from django.db.models.expressions import OrderBy
from django.db.models.fields import CharField
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here. 
class UserIncome(models.Model):
    amount = models.FloatField()
    date = models.DateField(default= now)
    description = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = CharField(max_length=256)

    def __str__(self):
        return self.source
    class Meta:
        ordering=['-date']
        verbose_name_plural='User Income'

class Source(models.Model):
        name = models.CharField(max_length=255)
        
        # class Meta:
        #     verbose_name_plural='Sources'
        
        
        def __str__(self):
            return self.name
        
    
    
