from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense/', views.add_expense, name='add-expenses'),
    path('expense-edit/<int:id>/', views.expenses_edit, name='expense-edit'),
    path('delete-expense/<int:id>',views.delete_expense, name='delete-expense'),
    path('search-expenses/', csrf_exempt(views.search_expense), name='search-expense'),
    path('expense_category_summary/', views.expense_category_summary, name='expense_category_summary'),
    path('stats/', views.stats_view, name='stats'),
    path('export-csv/', views.export_csv, name='export-csv'),
    path('export-excel/', views.export_excel, name='export-excel'),
    path('export-pdf/', views.export_pdf, name='export-pdf'),
]