from django import forms
from .models import Project,Expense,Contribution,Category


class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields = '__all__'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        fields='__all__'

class ContributionForm(forms.ModelForm):
    class Meta:
        model=Contribution
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'

