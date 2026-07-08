from django import forms
from .models import Project,Expense,Contribution,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['username'].widget.attrs['placeholder'] = 'اسم المستخدم'
        self.fields['password1'].widget.attrs['placeholder'] = 'كلمة المرور'
        self.fields['password2'].widget.attrs['placeholder'] = 'تأكيد كلمة المرور'

