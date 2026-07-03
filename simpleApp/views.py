from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum,Count
from .models import Project,Expense,Category,Contribution
from .forms import ProjectForm,ExpenseForm,ContributionForm,CategoryForm

# Create your views here.
def dashboard(request):
    projectN = Project.objects.count()
    expenseN = Expense.objects.count()
    contributionN =Contribution.objects.count()

    expenseT = Expense.objects.aggregate(total=Sum('value'))['total'] or 0
    contributionT = Contribution.objects.aggregate(total=Sum('amount'))['total'] or 0

    last_expenses=Expense.objects.order_by('-date')[:5]
    last_contribution=Contribution.objects.order_by('-date')[:5]


    context ={
        'projectNum':projectN,
        'expenseNum':expenseN,
        'contributionNum':contributionN,
        'totalExpense':expenseT,
        'totalContribution':contributionT,
        'last_exp':last_expenses,
        'last_cont':last_contribution,
    }
    return render(request,'simpleApp/dashboard.html',context)

def projects(request):
    projects=Project.objects.all()


    context={
        'projectsH':projects,
    }
    return render(request,'simpleApp/projects.html',context)

def project_details(request,id):
    project =get_object_or_404(Project, id=id)
    total_contributions = Contribution.objects.filter(project=project).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Expense.objects.filter(project=project).aggregate(total=Sum('value'))['total'] or 0
    funding_percentage =(total_contributions / project.budget) * 100 if project.budget else 0
    surplus =max(total_contributions - project.budget, 0)
    over_budget = total_expenses > project.budget


    contributors = Contribution.objects.filter(project=project)\
                    .values('name')\
                    .annotate(total=Sum('amount'))

    total_contributions1 = sum([c['total'] for c in contributors])

    for c in contributors:
        c['percentage'] = (c['total'] / total_contributions) * 100 if total_contributions else 0
    
    over_amount = max(total_expenses - total_contributions, 0)

    context = {
        'project': project,
        'total_contributions': total_contributions,
        'total_expenses': total_expenses,
        'funding_percentage': funding_percentage,
        'surplus': surplus,
        'over_budget': over_budget,
        'project': project,
        'total_contributions': total_contributions1,
        'contributors': contributors,
        'over_amount':over_amount,
    }
    return render(request,'simpleApp/project_details.html',context)

def expenses(request):
    expenses=Expense.objects.all()
    context={
        'expensesH':expenses
    }
    return render(request,'simpleApp/expenses.html',context)

def add_expense(request):
    if request.method =='POST':
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
            return redirect('expenses')
    else:
        expense = ExpenseForm()

    context={
        'expense':expense
    }
    return render(request,'simpleApp/add_expense.html',context)

def delete_expense(request,id):
    expense=get_object_or_404(Expense,id=id)
    expense.delete()
    return redirect('expenses')

def expense_details(request,id):
    expense =get_object_or_404(Expense,id=id)
    context={
        'expense':expense
    }
    return render(request,'simpleApp/expense_details.html',context)
    

def edit_expense(request,id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':
        eform = ExpenseForm(request.POST, instance=expense)
        if eform.is_valid():
            eform.save()
            return redirect('expenses')
    else:
        eform = ExpenseForm(instance=expense)

    context = {
        'eform': eform
    }
    return render(request,'simpleApp/edit_expense.html',context)


    

def contributions(request):
    contribution = Contribution.objects.all()

    context={
        'contributionH':contribution
    }

    return render(request,'simpleApp/contributions.html',context)

def add_contribution(request):
    if request.method=='POST':
        cform=ContributionForm(request.POST)
        if cform.is_valid():
            cform.save()
            return redirect('contributions')
    else:
        cform=ContributionForm()

    context={
        'cform':cform
    }
    return render(request,'simpleApp/add_contribution.html',context)


def delete_contribution(request,id):
    contribution=get_object_or_404(Contribution,id=id)
    contribution.delete()

    return redirect('contributions') 
    


def edit_contribution(request,id):
    contribution = get_object_or_404(Contribution,id=id)
    if request.method=='POST':
        cform = ContributionForm(request.POST,instance=contribution)
        if cform.is_valid():
            cform.save()
            return redirect('contributions')
    else:
        cform=ContributionForm(instance=contribution)

    context={
        'cform':cform
    }
    return render(request,'simpleApp/edit_contribution.html',context)

def contribution_details(request, id):
    contribution =get_object_or_404(Contribution,id=id)
    context={
        'contributionH':contribution
    }
    return render(request,'simpleApp/contribution_details.html',context)

def add_project(request):
    if request.method =='POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm()

    context={
        'form':form
    }
    return render(request,'simpleApp/add_project.html',context)

def delete_project(request,id):
    project=get_object_or_404(Project,id=id)
    project.delete()
    return redirect('projects')

def edit_project(request,id):
    project= get_object_or_404(Project, id=id)
    if request.method == "POST":
        form=ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    context={
        'form':form
    }
    return render(request,'simpleApp/edit_project.html',context)


def categories(request):
    categories=Category.objects.all()
    context={
        'categoriesH':categories
    }
    return render(request,'simpleApp/categories.html',context)

def add_category(request):
    if request.method =='POST':
        catForm = CategoryForm(request.POST)
        if catForm.is_valid():
            catForm.save()
            return redirect('categories')
    else:
        catForm=CategoryForm()
    
    context={
        'catFormH':catForm
    }

    return render(request,'simpleApp/add_category.html',context)

def delete_category(request,id):
    cat=get_object_or_404(Category,id=id)
    cat.delete()
    return redirect('categories')


def edit_category(request,id):
    cat= get_object_or_404(Category,id=id)
    if request.method=='POST':
        catForm=CategoryForm(request.POST,instance=cat)
        if catForm.is_valid():
            catForm.save()
            return redirect('categories')
    else:
        catForm=CategoryForm(instance=cat)
    
    context={
        'catFormH':catForm
    }
    return render(request,'simpleApp/edit_category.html',context)

def contributers(request):
    
    data = (Contribution.objects.values('name','project__name').annotate(total=Sum('amount'), count=Count('id')))

     # حساب مجموع كل مشروع
    project_totals = {}

    for item in Contribution.objects.values('project__name').annotate(total=Sum('amount')):
        project_totals[item['project__name']] = item['total']

    # إضافة النسبة
    for item in data:
        project_name = item['project__name']
        project_total = project_totals[project_name]

        item['percentage'] = round((item['total'] / project_total) * 100, 2)


    context={
        'contributors':data

    }
    return render(request,'simpleApp/contributers.html',context)
    