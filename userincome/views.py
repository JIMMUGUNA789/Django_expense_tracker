from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Source, UserIncome
from userpreferences.models import UserPreference
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    source = Source.objects.all()
    currency = UserPreference.objects.get(user=request.user).currency
    income = UserIncome.objects.filter(user_id=request.user.pk)
    paginator = Paginator(income, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'income':income,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'income/index.html', context)
    
def add_income(request):
    source = Source.objects.all()
    context = {
            'source': source,
            'values':request.POST
        }
    if request.method == 'GET':
        
        return render(request, 'income/add_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
    
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        
        income = UserIncome.objects.create(user_id=request.user.pk, amount=amount, date=date, description=description, source=source)
        income.save()
        messages.success(request, 'Income saved successfully')
        
        
    return redirect('income')

def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    source = Source.objects.all()
    context = {
        'income':income,
        'values':income,
        'source':source
    }
    if request.method=='GET':
      
        return render(request, 'income/edit_income.html', context)
    else:
          if request.method=='POST':
                amount = request.POST['amount']
                if not amount:
                    messages.error(request, 'Amount is required')
                    return render(request, 'income/edit_income.html', context)
            
                description = request.POST['description']
                date = request.POST['income_date']
                source = request.POST['source']
                if not description:
                    messages.error(request, 'Description is required')
                    return render(request, 'income/edit_income.html', context)
                
                
                income.user_id=request.user.pk
                income.amount=amount
                income.date=date
                income.description=description
                income.source=source
                income.save()
   
                messages.info(request, 'Changes saved successfully')
                return redirect('income')
def delete_income(request, id):
     UserIncome.objects.get(pk=id).delete()
     messages.warning(request, 'Income deleted')
     return redirect('income')

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, user=request.user) | UserIncome.objects.filter(
        date__istartswith=search_str, user=request.user) | UserIncome.objects.filter(
        description__icontains=search_str, user=request.user) | UserIncome.objects.filter(
        source__icontains=search_str, user=request.user)
        
        data = income.values()
        return JsonResponse(list(data), safe=False)

