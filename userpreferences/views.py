from pdb import Pdb
import pdb
from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

# Create your views here.
def index(request):
    exists = UserPreference.objects.filter(user=request.user).exists()
    if  exists:
        user_preferences = UserPreference.objects.get(user=request.user) 
    else:
        user_preferences = None
    


       
    currency_data = []  
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
            #open file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
        for key, value in data.items():  
            currency_data.append({'name':key, 'value':value})
       # import pdb ; pdb.set_trace()   
  
   
        
    if request.method == "GET":
                 
        
        return render(request, 'preferences/index.html', {'currencies':currency_data, 'user_preferences':user_preferences})
    else:
        currency = request.POST['currency'] 
        if exists:
             user_preferences.currency = currency  
             user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency).save()
            user_preferences = UserPreference.objects.get(user=request.user) 

        
              
        messages.success(request, 'Changes saved sucessfully')               
        return render(request, 'preferences/index.html', {'currencies':currency_data, 'user_preferences':user_preferences} )
