from django.urls import path
from . import views




urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('projects',views.projects,name='projects'),
    path('projects/add/',views.add_project,name='add_project'),
    path('projects/<int:id>/delete',views.delete_project,name="delete_project"),
    path('project/<int:id>/edit',views.edit_project,name='edit_project'),
    path('project_details/<int:id>',views.project_details,name='project_details'),
    path('expenses',views.expenses,name='expenses'),
    path('expenses/add/',views.add_expense,name='add_expense'),
    path('expenses/<int:id>/delete',views.delete_expense,name='delete_expense'),
    path('expenses/<int:id>/edit',views.edit_expense,name='edit_expense'),
    path('expenses/<int:id>',views.expense_details,name='expense_details'),
    path('contributions',views.contributions,name='contributions'),
    path('contributions/add/',views.add_contribution,name='add_contribution'),
    path('contributions/<int:id>/delete',views.delete_contribution,name='delete_contribution'),
    path('contributions/<int:id>/edit',views.edit_contribution,name='edit_contribution'),
    path('contributions/<int:id>',views.contribution_details,name='contribution_details'),
    path('categories',views.categories,name='categories'),
    path('categories/add',views.add_category,name='add_category'),
    path('categories/<int:id>/delete',views.delete_category,name='delete_category'),
    path('categories/<int:id>/edit',views.edit_category,name='edit_category'),
    path('contributers',views.contributers,name='contributers'),
    
]