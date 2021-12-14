from django.contrib import admin
from .models import UserIncome, Source

# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'source', 'description')
    list_per_page = 6
admin.site.register(UserIncome, IncomeAdmin)
admin.site.register(Source)
