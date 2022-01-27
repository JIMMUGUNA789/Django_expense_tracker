from django.core import paginator
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse, response
from userpreferences.models import UserPreference
import datetime
import csv
import  xlwt
import tempfile
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Sum


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    currency = UserPreference.objects.get(user=request.user).currency
    expenses = Expense.objects.filter(user_id=request.user.pk)
    paginator = Paginator(expenses, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'expenses/index.html', context)
    
def add_expense(request):
    categories = Category.objects.all()
    context = {
            'categories': categories,
            'values':request.POST
        }
    if request.method == 'GET':
        
        return render(request, 'expenses/add_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
    
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        
        expense = Expense.objects.create(user_id=request.user.pk, amount=amount, date=date, description=description, category=category)
        expense.save()
        messages.success(request, 'Expense saved successfully')
        
        
    return redirect('expenses')

def expenses_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories
    }
    if request.method=='GET':
      
        return render(request, 'expenses/edit_expense.html', context)
    else:
          if request.method=='POST':
                amount = request.POST['amount']
                if not amount:
                    messages.error(request, 'Amount is required')
                    return render(request, 'expenses/edit_expense.html', context)
            
                description = request.POST['description']
                date = request.POST['expense_date']
                category = request.POST['category']
                if not description:
                    messages.error(request, 'Description is required')
                    return render(request, 'expenses/edit_expense.html', context)
                
                
                expense.user_id=request.user.pk
                expense.amount=amount
                expense.date=date
                expense.description=description
                expense.category=category
                expense.save()
   
                messages.info(request, 'Changes saved successfully')
                return redirect('expenses')
def delete_expense(request, id):
     Expense.objects.get(pk=id).delete()
     messages.warning(request, 'Expense deleted')
     return redirect('expenses')

def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, user=request.user) | Expense.objects.filter(
        date__istartswith=search_str, user=request.user) | Expense.objects.filter(
        description__icontains=search_str, user=request.user) | Expense.objects.filter(
        category__icontains=search_str, user=request.user)
        
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(user=request.user, date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}
    
    def get_category(expense):
        return expense.category
    #use map function to call function for every item in expenses and use set to remove duplicates
    category_list = list(set(map(get_category, expenses)))
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount
    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)
    
    return JsonResponse({'expense_category_data':finalrep}, safe=False)

def stats_view(request):
    return render(request, 'expenses/stats.html')

#export data to different file formats
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+ str(datetime.datetime.now()) +'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])
    expenses = Expense.objects.filter(user=request.user)
    for expense in expenses:
        writer.writerow([expense.amount,expense.description, expense.category, expense.date])
    return response
def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+ str(datetime.datetime.now()) +'.xls'
    #create workbook
    wb = xlwt.Workbook(encoding='utf-8')
    #create a worksheet
    ws = wb.add_sheet('expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount', 'Descrition', 'Category', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(user = request.user).values_list('amount','description', 'category', 'date')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    #add sheet to workbook
    wb.save(response)
    
    return response


def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses'+ str(datetime.datetime.now()) +'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    expenses = Expense.objects.filter(user=request.user)
    sum = expenses.aggregate(Sum('amount'))
    html_string = render_to_string('expenses/pdf-output.html', {'expenses':expenses ,'total':sum['amount-sum']})
    html = HTML(string=html_string)
    result = html.write_pdf()
    #store pdf in mem while rendering it
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output=open(output.name, 'rb')
        response.write(output.read())
    
    
    return response
    
    


        
    
            
        
            
    


