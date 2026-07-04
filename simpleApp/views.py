from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from .models import Project, Expense, Category, Contribution
from .forms import ProjectForm, ExpenseForm, ContributionForm, CategoryForm
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("dashboard OK")
# ---------------- DASHBOARD ----------------
# def dashboard(request):
#     projectN = Project.objects.count()
#     expenseN = Expense.objects.count()
#     contributionN = Contribution.objects.count()

#     expenseT = Expense.objects.aggregate(total=Sum('value'))['total'] or 0
#     contributionT = Contribution.objects.aggregate(total=Sum('amount'))['total'] or 0

#     last_expenses = Expense.objects.order_by('-date')[:5]
#     last_contribution = Contribution.objects.order_by('-date')[:5]

#     context = {
#         'projectNum': projectN,
#         'expenseNum': expenseN,
#         'contributionNum': contributionN,
#         'totalExpense': expenseT,
#         'totalContribution': contributionT,
#         'last_exp': last_expenses,
#         'last_cont': last_contribution,
#     }
#     return render(request, 'simpleApp/dashboard.html', context)


# ---------------- PROJECTS ----------------
def projects(request):
    projects = Project.objects.all()
    return render(request, 'simpleApp/projects.html', {'projectsH': projects})


def project_details(request, id):
    project = get_object_or_404(Project, id=id)

    total_contributions = Contribution.objects.filter(project=project).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expenses = Expense.objects.filter(project=project).aggregate(
        total=Sum('value')
    )['total'] or 0

    funding_percentage = (
        (total_contributions / project.budget) * 100
        if project.budget else 0
    )

    surplus = max(total_contributions - project.budget, 0)
    over_budget = total_expenses > project.budget

    # ⚠️ IMPORTANT: تأكد اسم الحقل في موديل Contribution
    # إذا عندك ForeignKey اسمها contributor هذا صح
    # إذا اسمها user أو name غيره لازم تعدله هنا

    contributors = (
        Contribution.objects.filter(project=project)
        .values('name')
        .annotate(total=Sum('amount'))
    )

    for c in contributors:
        c['percentage'] = (
            (c['total'] / total_contributions) * 100
            if total_contributions > 0 else 0
        )

    over_amount = max(total_expenses - total_contributions, 0)

    context = {
        'project': project,
        'total_contributions': total_contributions,
        'total_expenses': total_expenses,
        'funding_percentage': funding_percentage,
        'surplus': surplus,
        'over_budget': over_budget,
        'contributors': contributors,
        'over_amount': over_amount,
    }

    return render(request, 'simpleApp/project_details.html', context)


# ---------------- EXPENSES ----------------
def expenses(request):
    expenses = Expense.objects.all()
    return render(request, 'simpleApp/expenses.html', {'expensesH': expenses})


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = ExpenseForm()

    return render(request, 'simpleApp/add_expense.html', {'expense': form})


def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expenses')


def expense_details(request, id):
    expense = get_object_or_404(Expense, id=id)
    return render(request, 'simpleApp/expense_details.html', {'expense': expense})


def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'simpleApp/edit_expense.html', {'eform': form})


# ---------------- CONTRIBUTIONS ----------------
def contributions(request):
    contribution = Contribution.objects.all()
    return render(request, 'simpleApp/contributions.html', {'contributionH': contribution})


def add_contribution(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contributions')
    else:
        form = ContributionForm()

    return render(request, 'simpleApp/add_contribution.html', {'cform': form})


def delete_contribution(request, id):
    contribution = get_object_or_404(Contribution, id=id)
    contribution.delete()
    return redirect('contributions')


def edit_contribution(request, id):
    contribution = get_object_or_404(Contribution, id=id)

    if request.method == 'POST':
        form = ContributionForm(request.POST, instance=contribution)
        if form.is_valid():
            form.save()
            return redirect('contributions')
    else:
        form = ContributionForm(instance=contribution)

    return render(request, 'simpleApp/edit_contribution.html', {'cform': form})


def contribution_details(request, id):
    contribution = get_object_or_404(Contribution, id=id)
    return render(request, 'simpleApp/contribution_details.html', {'contributionH': contribution})


# ---------------- PROJECT CRUD ----------------
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm()

    return render(request, 'simpleApp/add_project.html', {'form': form})


def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect('projects')


def edit_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'simpleApp/edit_project.html', {'form': form})


# ---------------- CATEGORIES ----------------
def categories(request):
    categories = Category.objects.all()
    return render(request, 'simpleApp/categories.html', {'categoriesH': categories})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'simpleApp/add_category.html', {'catFormH': form})


def delete_category(request, id):
    cat = get_object_or_404(Category, id=id)
    cat.delete()
    return redirect('categories')


def edit_category(request, id):
    cat = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=cat)

    return render(request, 'simpleApp/edit_category.html', {'catFormH': form})


# ---------------- CONTRIBUTORS REPORT ----------------
def contributers(request):
    data = Contribution.objects.values(
        'name',
        'project__name'
    ).annotate(
        total=Sum('amount'),
        count=Count('id')
    )

    project_totals = {
        item['project__name']: item['total']
        for item in Contribution.objects.values('project__name').annotate(total=Sum('amount'))
    }

    for item in data:
        project_name = item['project__name']
        project_total = project_totals.get(project_name,0)

        if project_total > 0:
            item['percentage'] = round((item['total'] / project_total) * 100, 2)
        else:
            item['percentage'] = 0

    return render(request, 'simpleApp/contributers.html', {
        'contributors': data
    })