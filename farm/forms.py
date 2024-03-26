from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['national_ID', 'name', 'email', 'phone', 'address', 'position', 'salary','date_employed']

class UnpaidMonthsForm(forms.ModelForm):
    class Meta:
        model = PaymentStatus
        fields = ['unpaid_months']

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_name', 'planting_date', 'harvesting_date', 'yield_amount', 'notes']

class CropHarvestedForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['harvesting_date', 'yield_amount',]

    def __init__(self, *args, **kwargs):
        super(CropHarvestedForm, self).__init__(*args, **kwargs)

class LivestockForm(forms.ModelForm):
    class Meta:
        model = Livestock
        fields = ['livestock_type', 'livestock_breed', 'quantity', 'health_status', 'notes']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'date', 'description']

    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)

class GoalAchievementForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['achievement_date']

    def __init__(self, *args, **kwargs):
        super(GoalAchievementForm, self).__init__(*args, **kwargs)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'date', 'deadline']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

class TaskCompletionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completion_date']

    def __init__(self, *args, **kwargs):
        super(TaskCompletionForm, self).__init__(*args, **kwargs)

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['category', 'product_name', 'quantity', 'unit_price', 'date', 'notes']

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)

        categories = ['crop', 'livestock', 'other'] #oher to hold sale not related to farm product eg sellin equipments
        self.fields['category'].queryset = categories

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'expense_name', 'description', 'cost', 'date']