from django.contrib import admin
from .models import Project,Expense,Category,Contribution,Transfer

# Register your models here.
admin.site.register(Project)
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Contribution)
admin.site.register(Transfer)