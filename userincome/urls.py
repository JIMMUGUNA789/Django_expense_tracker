from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='income'),
    path('add-income/', views.add_income, name='add-income'),
    path('income-edit/<int:id>/', views.income_edit, name='income-edit'),
    path('delete-income/<int:id>',views.delete_income, name='delete-income'),
    path('search-income/', csrf_exempt(views.search_income), name='search-income'),
]