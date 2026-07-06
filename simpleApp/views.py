from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from .models import Project, Expense, Category, Contribution
from .forms import ProjectForm, ExpenseForm, ContributionForm, CategoryForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    # المشاريع الخاصة بالمستخدم
    projects = Project.objects.filter(user=request.user)

    projectN = projects.count()

    # كل expenses الخاصة بمشاريع المستخدم
    expenses = Expense.objects.filter(project__user=request.user)
    expenseN = expenses.count()

    # كل contributions الخاصة بالمستخدم
    contributions = Contribution.objects.filter(project__user=request.user)
    contributionN = contributions.count()

    expenseT = expenses.aggregate(total=Sum('value'))['total'] or 0
    contributionT = contributions.aggregate(total=Sum('amount'))['total'] or 0

    last_expenses = expenses.order_by('-date')[:5]
    last_contribution = contributions.order_by('-date')[:5]

    context = {
        'projects':projects,
        'projectNum': projectN,
        'expenseNum': expenseN,
        'contributionNum': contributionN,
        'totalExpense': expenseT,
        'totalContribution': contributionT,
        'last_exp': last_expenses,
        'last_cont': last_contribution,
    }

    return render(request, 'simpleApp/dashboard.html', context)


# ---------------- PROJECTS ----------------
@login_required
def projects(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'simpleApp/projects.html', {'projectsH': projects})

@login_required
def project_details(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)

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
@login_required
def expenses(request):
    expenses = Expense.objects.filter(project__user=request.user)

    category = request.GET.get('category')
    if category:
        expenses = expenses.filter(category_id=category)

    categories = Category.objects.all()

    context = {
        "expenses": expenses,
        "categories": categories,
    }
    return render(request, 'simpleApp/expenses.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)

            # تأكد أن المشروع تابع للمستخدم
            expense.project = get_object_or_404(
                Project,
                id=request.POST.get('project'),
                user=request.user
            )

            expense.save()
            return redirect('expenses')
    else:
        form = ExpenseForm()

    return render(request, 'simpleApp/add_expense.html', {'expense': form})

@login_required
def delete_expense(request, id):
    expense = get_object_or_404(
        Expense,
        id=id,
        project__user=request.user
    )

    expense.delete()
    return redirect('expenses')

@login_required
def expense_details(request, id):
    expense = get_object_or_404(
        Expense,
        id=id,
        project__user=request.user
    )

    return render(request, 'simpleApp/expense_details.html', {'expense': expense})
@login_required
def edit_expense(request, id):
    expense = get_object_or_404(
        Expense,
        id=id,
        project__user=request.user
    )

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'simpleApp/edit_expense.html', {'eform': form})


# ---------------- CONTRIBUTIONS ----------------
@login_required
def contributions(request):
    contribution = Contribution.objects.filter(project__user=request.user)
    return render(request, 'simpleApp/contributions.html', {'contributionH': contribution})

@login_required
def add_contribution(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)

        form.fields['project'].queryset = Project.objects.filter(user=request.user)

        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.save()
            return redirect('contributions')
    else:
        form = ContributionForm()
        form.fields['project'].queryset = Project.objects.filter(user=request.user)

    return render(request, 'simpleApp/add_contribution.html', {'cform': form})

@login_required
def delete_contribution(request, id):
    contribution = get_object_or_404(
        Contribution,
        id=id,
        project__user=request.user
    )

    if request.method == "POST":
        contribution.delete()

    return redirect('contributions')

@login_required
def edit_contribution(request, id):
    contribution = get_object_or_404(
        Contribution,
        id=id,
        project__user=request.user
    )

    if request.method == 'POST':
        form = ContributionForm(request.POST, instance=contribution)
        if form.is_valid():
            form.save()
            return redirect('contributions')
    else:
        form = ContributionForm(instance=contribution)

    return render(request, 'simpleApp/edit_contribution.html', {'cform': form})

@login_required
def contribution_details(request, id):
    contribution = get_object_or_404(
        Contribution,
        id=id,
        project__user=request.user
    )

    return render(request, 'simpleApp/contribution_details.html', {'contributionH': contribution})


# ---------------- PROJECT CRUD ----------------
@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)  # ما نحفظوش مباشرة
            project.user = request.user        # 👈 ربط المشروع بالمستخدم
            project.save()

            return redirect('projects')
    else:
        form = ProjectForm()

    return render(request, 'simpleApp/add_project.html', {'form': form})

@login_required
def delete_project(request, id):
    project = get_object_or_404(
        Project,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        project.delete()
        return redirect('projects')

    return render(request, 'simpleApp/delete_project.html', {'project': project})

@login_required
def edit_project(request, id):
    project = get_object_or_404(
        Project,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'simpleApp/edit_project.html', {'form': form})


# ---------------- CATEGORIES ----------------
@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, 'simpleApp/categories.html', {'categoriesH': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'simpleApp/add_category.html', {'catFormH': form})

@login_required
def delete_category(request, id):
    cat = get_object_or_404(Category, id=id)
    cat.delete()
    return redirect('categories')

@login_required
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
@login_required
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

#---------------------------------------------login_view-------------------------
def loginv(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user =authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request, "simpleApp/login.html", {"error": "بيانات غير صحيحة"})
    return render(request, "simpleApp/login.html")




@login_required  # ❌ لا تضعها هنا (خطأ شائع)
def signupv(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # يدخل مباشرة بعد التسجيل
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'simpleApp/signup.html', {'form': form})