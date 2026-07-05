from django import forms
from .models import Project,Expense,Contribution,Category


class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'اسم المشروع'
            }),
            'project_details': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 3,
                'placeholder': 'وصف المشروع'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'الميزانية'
            }),
            'status': forms.Select(attrs={
            'class': 'form-select rounded-3'
            }),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        fields='__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'اسم المصروف'
            }),

            'value': forms.NumberInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'القيمة'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),

            'project': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
        }
        

class ContributionForm(forms.ModelForm):
    class Meta:
        model=Contribution
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'اسم السهم'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'القيمة'
            }),

            'project': forms.Select(attrs={
                'class': 'form-select rounded-3'
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-3',
                'placeholder': 'اسم فئة'
            }),}

