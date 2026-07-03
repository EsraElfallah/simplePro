from django.db import models

# Create your models here.
class Project(models.Model):
    STATUS_CHOICES=[
        ('planning','قيد التخطيط'),
        ('active','قيد التنفيذ'),
        ('paused','متوقف'),
        ('completed','منجز'),
    ]

    name=models.CharField(max_length=255,default='project')
    project_details=models.TextField()
    budget=models.DecimalField(max_digits=12,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name=models.CharField(max_length=255,default='مواد')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    name=models.CharField(max_length=255,default='expense')
    value=models.DecimalField(max_digits=12,decimal_places=2)
    #expense_category
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categories')
    #which_project_expense
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='expenses')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contribution(models.Model):
    name=models.CharField(max_length=255)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    #contribution_which_project
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='contributions')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Transfer(models.Model):
    from_project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='out_transfers')
    to_project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='in_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.amount} from {self.from_project} to {self.to_project}'