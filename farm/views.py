from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Avg
from .forms import *
from .models import *
from datetime import date
from django.contrib.auth.views import PasswordChangeView

class Index(TemplateView):
    template_name = 'farm/index.html'

class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        employees = Employee.objects.filter(user=self.request.user.id)
        username = self.request.user.username

        tasks = Task.objects.filter(user=request.user).all()
        active_tasks = []
        for task in tasks:
            if task.completed == False:
                active_tasks.append(task)

        goals = Goal.objects.filter(user=request.user).all()
        active_goals = []
        for goal in goals:
            if goal.achieved == False:
                active_goals.append(goal)

        total_expense_cost = Expense.objects.filter(user=request.user).aggregate(total_expenses=models.Sum('cost'))[
                                 'total_expenses'] or 0
        amounts = TotalAmountPaid.objects.all()
        total_amount_paid = sum(amount.total_amount for amount in amounts)
        total_expense = total_expense_cost + total_amount_paid
        total_sale = Sale.objects.filter(user=request.user).aggregate(total_sales=models.Sum('total_amount'))[
                         'total_sales'] or 0
        net_benefit = total_sale - total_expense
        profit_loss = "profit" if net_benefit >= 0 else "loss"

        expenses = Expense.objects.filter(user=request.user)
        crop_expenses = []
        livestock_expenses = []
        other_expenses = []
        for expense in expenses:
            if expense.category == 'crop':
                crop_expenses.append(expense)
            if expense.category == 'livestock':
                livestock_expenses.append(expense)
            if expense.category == 'other':
                other_expenses.append(expense)
        total_crop_expenses = sum(expense.cost for expense in crop_expenses)
        total_livestock_expenses = sum(expense.cost for expense in livestock_expenses)
        total_other_expenses = sum(expense.cost for expense in other_expenses)

        sales = Sale.objects.filter(user=request.user)
        crop_sales = []
        livestock_sales = []
        other_sales = []
        for sale in sales:
            if sale.category == 'crop':
                crop_sales.append(sale)
            if sale.category == 'livestock':
                livestock_sales.append(sale)
            if sale.category == 'other':
                other_sales.append(sale)
        total_crop_sales = sum(sale.total_amount for sale in crop_sales)
        total_livestock_sales = sum(sale.total_amount for sale in livestock_sales)
        total_other_sales = sum(sale.total_amount for sale in other_sales)

        try:
            percent_crop_sales = total_crop_sales / total_sale * 100
            percent_livestock_sales = total_livestock_sales / total_sale * 100
            percent_other_sales = total_other_sales / total_sale * 100
            percent_crop_exp = total_crop_expenses/total_expense * 100
            percent_livestock_exp = total_livestock_expenses/total_expense * 100
            percent_other_exp = total_other_expenses/total_expense * 100
            percent_employee_salary = total_amount_paid/total_expense * 100

        except ZeroDivisionError:
            percent_crop_exp = 0
            percent_livestock_exp = 0
            percent_other_exp = 0
            percent_crop_sales = 0
            percent_livestock_sales = 0
            percent_other_sales = 0
            percent_employee_salary = 0

        context = {
            'employees': employees,
            'username': username,
            'active_tasks': active_tasks,
            'active_goals': active_goals,
            'total_expense': total_expense,
            'total_sale': total_sale,
            'net_benefit': net_benefit,
            'profit_loss': profit_loss,
            'percent_crop_exp': percent_crop_exp,
            'percent_livestock_exp ': percent_livestock_exp,
            'percent_other_exp': percent_other_exp,
            'percent_employee_salary': percent_employee_salary,
            'percent_livestock_sales': percent_livestock_sales,
            'percent_crop_sales': percent_crop_sales,
            'percent_other_sales': percent_other_sales

        }
        return render(request, 'farm/dashboard.html', context)

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm
        return render(request, 'farm/signup.html', {'form':form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')

        return render(request, 'farm/signup.html')

def custom_logout(request):
    logout(request)
    return render(request, 'farm/logout.html')

# ***************************  E M P L O Y E E   M A N A G E M E N T  *******************************

class EmployeeView(LoginRequiredMixin,View):
    def get(self, request):
        employees = Employee.objects.filter(user=self.request.user.id).order_by('id')
        print(employees)
        return render(request, 'employee_mgmt/employee.html',{"employees":employees})

class EmployeePayment(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        employees = Employee.objects.filter(user=user)
        for employee in employees:
            if not PaymentStatus.objects.filter(employee=employee).exists():
                PaymentStatus.objects.create(employee=employee)
        employee_payment = PaymentStatus.objects.filter(employee__in=employees)
        return render(request, 'employee_mgmt/employee_payment.html', {"employee_payment": employee_payment})

class AddEmployee(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_mgmt/employee_form.html'
    success_url = reverse_lazy('employee-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteEmployee(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee_mgmt/delete_employee.html'
    success_url = reverse_lazy('employee-view')
    context_object_name = 'employee'

class EditEmployee(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_mgmt/edit_employee.html'
    success_url = reverse_lazy('employee-view')

    def get_form(self, form_class=None):
        form = super(EditEmployee, self).get_form(form_class)
        form.fields.pop('date_employed')  # Exclude date_employed field from the form
        return form

    def form_valid(self, form):
        instance = form.instance
        instance.date_employed = Employee.objects.get(pk=instance.pk).date_employed  # Set date_employed to the existing value
        return super().form_valid(form)

class EditUnpaidMonths(LoginRequiredMixin, UpdateView,):
    model = PaymentStatus
    form_class = UnpaidMonthsForm
    template_name = 'employee_mgmt/edit_unpaidmonths.html'
    success_url = reverse_lazy('payment-status')
    context_object_name = 'employee'


class MakePayments(LoginRequiredMixin, UpdateView):
    model = PaymentStatus
    form_class = UnpaidMonthsForm
    template_name = 'employee_mgmt/make_payments.html'
    success_url = reverse_lazy('payment-status')
    context_object_name = 'employee'

    def get_form(self, form_class=None):
        form = super(MakePayments, self).get_form(form_class)
        form.fields.pop('unpaid_months')  # Exclude unpaid_months field from the form
        return form

    def form_valid(self, form):
        instance = form.instance
        instance.unpaid_months = PaymentStatus.objects.get(pk=instance.pk).unpaid_months  # Set unpaid_months to the existing value
        if instance.unpaid_months == 0:
            messages.info(self.request, "No unpaid months. The employee has been paid for all the previous months.")
            return redirect('payment-status')

        elif instance.unpaid_months >= 1:
            instance.unpaid_months = instance.unpaid_months - 1
            emp_id = instance.pk
            paymentdate = date.today()
            employee_salary = Employee.objects.get(id=emp_id).salary

            try:
                old_amount_paid = TotalAmountPaid.objects.get(employee_id=emp_id).total_amount
                print(f"tptal amount paid is {old_amount_paid}")
                new_amount_paid = old_amount_paid + employee_salary
                paymentrecords = PaymentRecords(
                    employee_id=emp_id,
                    salary=employee_salary,
                    payment_date=paymentdate
                )
                paymentrecords.save()

                total_amount_paid = TotalAmountPaid(
                    employee_id=emp_id,
                    total_amount=new_amount_paid
                )
                total_amount_paid.save()

            except TotalAmountPaid.DoesNotExist:
                new_amount_paid = employee_salary
                paymentrecords = PaymentRecords(
                    employee_id=emp_id,
                    salary = employee_salary,
                    payment_date=paymentdate
                )
                paymentrecords.save()

                total_amount_paid = TotalAmountPaid(
                    employee_id=emp_id,
                    total_amount=new_amount_paid
                )
                total_amount_paid.save()


        elif instance.unpaid_months < 0:
            messages.info(self.request,"Value of unpaid months is invalid!")
            return redirect('payment-status')

        return super().form_valid(form)

class PaymentRecordsView(LoginRequiredMixin, View):
    def get(self, request):
        payment_records = PaymentRecords.objects.filter(employee_id__user_id=request.user.id).order_by('employee_id')
        #total_amount_paid = TotalAmountPaid.objects.aggregate(total=sum('total_amount'))['total'] or 0
        amounts = TotalAmountPaid.objects.all()
        total_amount_paid = sum(amount.total_amount for amount in amounts)
        print(payment_records)
        return render(request, 'employee_mgmt/payment_records.html', {"payment_records": payment_records, 'total_amount_paid': total_amount_paid})

# ***************************  C R O P   M A N A G E M E N T  *******************************
def crop_list(request):
    crops = Crop.objects.filter(user=request.user).all()
    return render(request, 'crop_mgmt/crop_list.html', {'crops': crops})

def add_crop(request):
    if request.method == 'POST':
        crop_form = CropForm(request.POST)
        if crop_form.is_valid():
            crop = crop_form.save(commit=False)
            crop.user_id = request.user.id
            crop.save()
            return redirect('crop_list')
    else:
        crop_form = CropForm()
    return render(request, 'crop_mgmt/add_crop.html', {'crop_form': crop_form})

def edit_crop(request, crop_id):
    crop = get_object_or_404(Crop, crop_id=crop_id)
    if request.method == 'POST':
        crop_form = CropForm(request.POST, instance=crop)
        if crop_form.is_valid():
            crop_form.save()
            return redirect('crop_list')
    else:
        crop_form = CropForm(instance=crop)
    return render(request, 'crop_mgmt/edit_crop.html', {'crop_form': crop_form, 'crop': crop})

class DeleteCrop(LoginRequiredMixin, DeleteView):
    model = Crop
    template_name = 'crop_mgmt/delete_crop.html'
    success_url = reverse_lazy('crop_list')
    context_object_name = 'crop'

def harvest_crop(request, crop_id):
    crop = get_object_or_404(Crop, crop_id=crop_id)
    if request.method == 'POST':
        crop_harvestedform = CropHarvestedForm(request.POST, instance=crop)
        if crop_harvestedform.is_valid():
            crop_harvested = crop_harvestedform.save(commit=False)
            crop_harvested.harvested = True
            crop_harvested.save()
            return redirect('crop_list')
    else:
        crop_harvestedform = CropHarvestedForm(request.POST, instance=crop)
    return render(request, 'crop_mgmt/harvest_crop.html', {'crop_harvestedform': crop_harvestedform, 'crop': crop})

# ***************************  L I V E S T O C K   M A N A G E M E N T  *******************************
def livestock_list(request):
    livestocks = Livestock.objects.filter(user=request.user).all()
    return render(request, 'livestock_mgmt/livestock_list.html', {'livestocks': livestocks})

def add_livestock(request):
    if request.method == 'POST':
        livestock_form = LivestockForm(request.POST)
        if livestock_form.is_valid():
            livestock = livestock_form.save(commit=False)
            livestock.user_id = request.user.id
            livestock.save()
            return redirect('livestock_list')
    else:
        livestock_form = LivestockForm()
    return render(request, 'livestock_mgmt/add_livestock.html', {'livestock_form': livestock_form})

def edit_livestock(request, livestock_id):
    livestock = get_object_or_404(Livestock, livestock_id=livestock_id)
    if request.method == 'POST':
        livestock_form = LivestockForm(request.POST, instance=livestock)
        if livestock_form.is_valid():
            livestock_form.save()
            return redirect('livestock_list')
    else:
        livestock_form = LivestockForm(instance=livestock)
    return render(request, 'livestock_mgmt/edit_livestock.html', {'livestock_form': livestock_form, 'livestock': livestock})

class DeleteLivestock(LoginRequiredMixin, DeleteView):
    model = Livestock
    template_name = 'livestock_mgmt/delete_livestock.html'
    success_url = reverse_lazy('livestock_list')
    context_object_name = 'livestock'

# ***************************  G O A L   M A N A G E M E N T  *******************************

def goal_list(request):
    goals = Goal.objects.filter(user=request.user).all()
    return render(request, 'goal_mgmt/goal_list.html', {'goals': goals})

def add_goal(request):
    if request.method == 'POST':
        goal_form = GoalForm(request.POST)
        if goal_form.is_valid():
            goal = goal_form.save(commit=False)
            goal.user_id = request.user.id
            goal.save()
            return redirect('goal_list')
    else:
        goal_form = GoalForm()
    return render(request, 'goal_mgmt/add_goal.html', {'goal_form': goal_form})

def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, goal_id=goal_id)
    if request.method == 'POST':
        goal_form = GoalForm(request.POST, instance=goal)
        if goal_form.is_valid():
            goal_form.save()
            return redirect('goal_list')
    else:
        goal_form = GoalForm(instance=goal)
    return render(request, 'goal_mgmt/edit_goal.html', {'goal_form': goal_form, 'goal': goal})

class DeleteGoal(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goal_mgmt/delete_goal.html'
    success_url = reverse_lazy('goal_list')
    context_object_name = 'goal'

def achieve_goal(request, goal_id):
    goal = get_object_or_404(Goal, goal_id=goal_id)
    if request.method == 'POST':
        goal_achievementform = GoalAchievementForm(request.POST, instance=goal)
        if goal_achievementform.is_valid():
            achieved_goal = goal_achievementform.save(commit=False)
            achieved_goal.achieved = True
            achieved_goal.save()
            return redirect('goal_list')
    else:
        goal_achievedform = GoalAchievementForm(request.POST, instance=goal)
    return render(request, 'goal_mgmt/achieve_goal.html', {'goal_achievedform': goal_achievedform, 'goal': goal})

def active_goal(request):
    goals = Goal.objects.filter(user=request.user).all()
    active_goals = []
    for goal in goals:
        if goal.achieved == False:
            active_goals.append(goal)
    return render(request, 'goal_mgmt/active_goal.html', {'active_goals': active_goals})

def achieved_goal(request):
    goals = Goal.objects.filter(user=request.user).all()
    achieved_goals = []
    for goal in goals:
        if goal.achieved== True:
            achieved_goals.append(goal)
    return render(request, 'goal_mgmt/achieved_goal.html', {'achieved_goals': achieved_goals})

# ***************************  T A S k   M A N A G E M E N T  *******************************

def task_list(request):
    tasks = Task.objects.filter(user=request.user).all()
    return render(request, 'task_mgmt/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user_id = request.user.id
            task.save()
            return redirect('task_list')
    else:
        task_form = TaskForm()
    return render(request, 'task_mgmt/add_task.html', {'task_form': task_form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('task_list')
    else:
        task_form = TaskForm(instance=task)
    return render(request, 'task_mgmt/edit_task.html', {'task_form': task_form, 'task': task})

class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_mgmt/delete_task.html'
    success_url = reverse_lazy('task_list')
    context_object_name = 'task'

def active_task(request):
    tasks = Task.objects.filter(user=request.user).all()
    active_tasks = []
    for task in tasks:
        if task.completed == False:
            active_tasks.append(task)
    return render(request, 'task_mgmt/active_task.html', {'active_tasks': active_tasks})

def completed_task(request):
    tasks = Task.objects.filter(user=request.user).all()
    completed_tasks = []
    for task in tasks:
        if task.completed == True:
            completed_tasks.append(task)
    return render(request, 'task_mgmt/completed_task.html', {'completed_tasks': completed_tasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    if request.method == 'POST':
        task_completionform = TaskCompletionForm(request.POST, instance=task)
        if task_completionform.is_valid():
            task_completion = task_completionform.save(commit=False)
            task_completion.completed = True
            task_completion.save()
            return redirect('task_list')
    else:
        task_completionform = TaskCompletionForm(instance=task)
    return render(request, 'task_mgmt/complete_task.html', {'task_completionform': task_completionform, 'task': task})

# ***************************  S A L E   M A N A G E M E N T  *******************************

def sale_list(request):
    category = request.GET.get('category')
    product_name = request.GET.get('product_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sales = Sale.objects.filter(user=request.user).all()
    if category:
        sales = sales.filter(category=category)
    if product_name:
        sales = sales.filter( product_name=product_name)
    if start_date:
        sales = sales.filter(date__gte=start_date)
    if end_date:
        sales = sales.filter(date__lte=end_date)

    categories = Sale.objects.filter(user=request.user).values_list('category', flat=True).distinct()
    product_names = Sale.objects.filter(user=request.user).values_list('product_name', flat=True).distinct()
    total_sales_amount = Sale.objects.filter(user=request.user).aggregate(total_amounts=models.Sum('total_amount'))[
                        'total_amounts'] or 0

    context = {
        'sales': sales,
        'categories': categories,
        'product_names': product_names,
        'total_sales_amount': total_sales_amount,
    }

    return render(request, 'sale_mgmt/sale_list.html', context)
def add_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.user_id = request.user.id
            sale.save()
            return redirect('sale_list')
    else:
        sale_form = SaleForm()
    return render(request, 'sale_mgmt/add_sale.html', {'sale_form': sale_form})

def edit_sale(request, sale_id):
    sale = get_object_or_404(Sale, sale_id=sale_id)
    if request.method == 'POST':
        sale_form = SaleForm(request.POST, instance=sale)
        if sale_form.is_valid():
            sale_form.save()
            return redirect('sale_list')
    else:
        sale_form = SaleForm(instance=sale)
    return render(request, 'sale_mgmt/edit_sale.html', {'sale_form': sale_form, 'sale': sale})

class DeleteSale(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale_mgmt/delete_sale.html'
    success_url = reverse_lazy('sale_list')
    context_object_name = 'sale'

# ***************************  E X P E N S E   M A N A G E M E N T  *******************************

def expense_list(request):
    category = request.GET.get('category')
    expense_name = request.GET.get('expense_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter expenses based on provided filters
    expenses = Expense.objects.filter(user=request.user).all()
    if category:
        expenses = expenses.filter(category=category)
    if expense_name:
        expenses = expenses.filter(expense_name=expense_name)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    categories = Expense.objects.filter(user=request.user).values_list('category', flat=True).distinct()
    expense_names = Expense.objects.filter(user=request.user).values_list('expense_name', flat=True).distinct()
    total_expense = Expense.objects.filter(user=request.user).aggregate(total_expenses=models.Sum('cost'))['total_expenses'] or 0

    context = {
        'expenses': expenses,
        'categories': categories,
        'expense_names': expense_names,
        'total_expense': total_expense,
    }

    return render(request, 'expense_mgmt/expense_list.html', context)

def add_expense(request):
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user_id = request.user.id
            expense.save()
            return redirect('expense_list')
    else:
        expense_form = ExpenseForm()
    return render(request, 'expense_mgmt/add_expense.html', {'expense_form': expense_form})

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, expense_id=expense_id)
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST, instance=expense)
        if expense_form.is_valid():
            expense_form.save()
            return redirect('expense_list')
    else:
        expense_form = ExpenseForm(instance=expense)
    return render(request, 'expense_mgmt/edit_expense.html', {'expense_form': expense_form, 'expense': expense})

class DeleteExpense(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expense_mgmt/delete_expense.html'
    success_url = reverse_lazy('expense_list')
    context_object_name = 'expense'

# ************************** S U M M A R Y    R E P O R T S *******************************

def financial_general_report(request):
    total_expense_cost = Expense.objects.filter(user=request.user).aggregate(total_expenses=models.Sum('cost'))[
                        'total_expenses'] or 0
    amounts = TotalAmountPaid.objects.all()
    total_amount_paid = sum(amount.total_amount for amount in amounts)
    total_expense = total_expense_cost + total_amount_paid
    total_sale = Sale.objects.filter(user=request.user).aggregate(total_sales=models.Sum('total_amount'))[
                        'total_sales'] or 0
    net_benefit = total_sale - total_expense
    profit_loss = "profit" if net_benefit >= 0 else "loss"

    expenses = Expense.objects.filter(user=request.user)
    crop_expenses = []
    livestock_expenses = []
    other_expenses = []
    for expense in expenses:
        if expense.category == 'crop':
            crop_expenses.append(expense)
        if expense.category == 'livestock':
            livestock_expenses.append(expense)
        if expense.category == 'other':
            other_expenses.append(expense)
    total_crop_expenses = sum(expense.cost for expense in crop_expenses)
    total_livestock_expenses = sum(expense.cost for expense in livestock_expenses)
    total_other_expenses = sum(expense.cost for expense in other_expenses)

    sales = Sale.objects.filter(user=request.user)
    crop_sales = []
    livestock_sales = []
    other_sales = []
    for sale in sales:
        if sale.category == 'crop':
            crop_sales.append(sale)
        if sale.category == 'livestock':
            livestock_sales.append(sale)
        if sale.category == 'other':
            other_sales.append(sale)
    total_crop_sales = sum(sale.total_amount for sale in crop_sales)
    total_livestock_sales = sum(sale.total_amount for sale in livestock_sales)
    total_other_sales = sum(sale.total_amount for sale in other_sales)

    context = {
        'total_expense': total_expense,
        'total_sale': total_sale,
        'total_crop_expenses': total_crop_expenses,
        'total_crop_sales': total_crop_sales,
        'total_livestock_expenses': total_livestock_expenses,
        'total_livestock_sales': total_livestock_sales,
        'total_other_expenses': total_other_expenses,
        'total_other_sales': total_other_sales,
        'total_amount_paid': total_amount_paid,
        'profit_loss': profit_loss,
        'net_benefit': net_benefit
    }
    return render(request, 'financial_report/general_financial_report.html', context)

def general_expense_summary(request):
    expenses = Expense.objects.filter(user=request.user)
    crop_expenses = []
    livestock_expenses = []
    other_expenses = []
    for expense in expenses:
        if expense.category == 'crop':
            crop_expenses.append(expense)
        if expense.category == 'livestock':
            livestock_expenses.append(expense)
        if expense.category == 'other':
            other_expenses.append(expense)
    total_crop_expenses = sum(expense.cost for expense in crop_expenses)
    total_livestock_expenses = sum(expense.cost for expense in livestock_expenses)
    total_other_expenses = sum(expense.cost for expense in other_expenses)
    amounts = TotalAmountPaid.objects.all()
    total_expense_cost = Expense.objects.filter(user=request.user).aggregate(total_expenses=models.Sum('cost'))[
                        'total_expenses'] or 0
    total_amount_paid = sum(amount.total_amount for amount in amounts)
    total_expense = total_expense_cost + total_amount_paid

    try:
        percent_crop_exp = total_crop_expenses/total_expense * 100
        percent_livestock_exp = total_livestock_expenses/total_expense * 100
        percent_other_exp = total_other_expenses/total_expense * 100
        percent_employee_salary = total_amount_paid/total_expense * 100

    except ZeroDivisionError:
        percent_crop_exp = 0
        percent_livestock_exp = 0
        percent_other_exp = 0
        percent_employee_salary = 0

    context = {
        'total_expense': total_expense,
        'total_crop_expenses': total_crop_expenses,
        'total_livestock_expenses': total_livestock_expenses,
        'total_other_expenses': total_other_expenses,
        'total_amount_paid': total_amount_paid,
        'percent_crop_exp': percent_crop_exp,
        'percent_livestock_exp ': percent_livestock_exp,
        'percent_other_exp': percent_other_exp,
        'percent_employee_salary': percent_employee_salary,

    }

    return render(request, 'expense_summary/general_expense_summary.html', context)

def detailed_crop_expense(request):
    expenses = Expense.objects.filter(user=request.user).all()
    crop_expenses = []
    crop_expense_names = []
    for expense in expenses:
        if expense.category == 'crop':
            crop_expenses.append(expense)
            crop_expense_names.append(expense.expense_name)
    expense_types = []
    for name in crop_expense_names:
        if name not in expense_types:
            expense_types.append(name)

    total_amount = sum(expense.cost for expense in crop_expenses)
    expense_by_type = [expenses.filter(expense_name=expense_type).aggregate(total=models.Sum('cost'))['total'] or 0 for expense_type in expense_types]
    expense_distribution = [float(amount) / float(total_amount) * 100 if total_amount > 0 else 0 for amount in expense_by_type]
    print(expense_types)
    print(expense_by_type)
    print(expense_distribution)
    context = {
        'crop_expenses': crop_expenses,
        'expense_types': expense_types,
        'expense_by_type': expense_by_type,
        'expense_distribution': expense_distribution,
    }
    return render(request, 'expense_summary/detailed_crop_expense_summary.html', context)

def detailed_livestock_expenses( request):
    expenses = Expense.objects.filter(user=request.user)
    livestock_expenses = []
    livestock_expense_names = []
    for expense in expenses:
        if expense.category == 'livestock':
            livestock_expenses.append(expense)
            livestock_expense_names.append(expense.expense_name)
    expense_types = []
    for name in livestock_expense_names:
        if name not in expense_types:
            expense_types.append(name)
    print(livestock_expenses)
    print(livestock_expense_names)
    print(expense_types)
    total_amount = sum(expense.cost for expense in livestock_expenses)
    expense_by_type = [expenses.filter(expense_name=expense_type).aggregate(total=models.Sum('cost'))['total'] or 0 for expense_type in expense_types]
    expense_distribution = [float(amount) / float(total_amount) * 100 if total_amount > 0 else 0 for amount in expense_by_type]

    context = {
        'livestock_expenses': livestock_expenses,
        'expense_types': expense_types,
        'expense_by_type': expense_by_type,
        'expense_distribution': expense_distribution,
    }
    return render(request, 'expense_summary/detailed_livestock_expense_summary.html', context)


def detailed_other_expense(request):
    expenses = Expense.objects.filter(user=request.user)
    other_expenses = []
    other_expense_names = []
    for expense in expenses:
        if expense.category == 'other':
            other_expenses.append(expense)
            other_expense_names.append(expense.expense_name)
    expense_types = []
    for name in other_expense_names:
        if name not in expense_types:
            expense_types.append(name)

    total_amount = sum(expense.cost for expense in other_expenses)
    expense_by_type = [expenses.filter(expense_name=expense_type).aggregate(total=models.Sum('cost'))['total'] or 0 for
                       expense_type in expense_types]
    expense_distribution = [float(amount) / float(total_amount) * 100 if total_amount > 0 else 0 for amount in
                            expense_by_type]

    context = {
        'other_expenses': other_expenses,
        'expense_types': expense_types,
        'expense_by_type': expense_by_type,
        'expense_distribution': expense_distribution,
    }
    return render(request, 'expense_summary/detailed_other_expense_summary.html', context)

def general_sale_summary(request):
    sales = Sale.objects.filter(user=request.user)
    crop_sales = []
    livestock_sales = []
    other_sales = []
    for sale in sales:
        if sale.category == 'crop':
            crop_sales.append(sale)
        if sale.category == 'livestock':
            livestock_sales.append(sale)
        if sale.category == 'other':
            other_sales.append(sale)
    total_crop_sales = sum(sale.total_amount for sale in crop_sales)
    total_livestock_sales = sum(sale.total_amount for sale in livestock_sales)
    total_other_sales = sum(sale.total_amount for sale in other_sales)
    total_sale = Sale.objects.filter(user=request.user).aggregate(total_sales=models.Sum('total_amount'))[
                        'total_sales'] or 0
    try:
        percent_crop_sale = total_crop_sales/total_sale * 100
        percent_livestock_sale = total_livestock_sales/total_sale * 100
        percent_other_sales = total_other_sales/total_sale * 100

    except ZeroDivisionError:
        percent_crop_sale = 0
        percent_other_sales = 0
        percent_livestock_sale = 0

    context = {
        'total_sale': total_sale,
        'total_livestock_sales': total_livestock_sales,
        'total_crop_sales': total_crop_sales,
        'total_other_sales': total_other_sales,
        'percent_livestock_sales': percent_livestock_sale,
        'percent_crop_sales': percent_crop_sale,
        'percent_other_sales': percent_other_sales
    }
    return render(request, 'sale_summary/general_sale_summary.html', context)

def detailed_crop_sale(request):
    sales = Sale.objects.filter(user=request.user).all()
    crop_sales = []
    crop_sales_names = []
    for sale in sales:
        if sale.category == 'crop':
            crop_sales.append(sale)
            crop_sales_names.append(sale.product_name)
    product_types = []
    for name in crop_sales_names:
        if name not in product_types:
            product_types.append(name)

    total_amount = sum(sale.total_amount for sale in crop_sales)
    sale_by_type = [sales.filter(product_name=product_type).aggregate(total=models.Sum('total_amount'))['total'] or 0 for product_type in product_types]
    sale_distribution = [float(amount) / float(total_amount) * 100 if total_amount > 0 else 0 for amount in sale_by_type]
    print(product_types)
    print(sale_by_type)
    print(sale_distribution)
    context = {
        'crop_sales': crop_sales,
        'product_types': product_types,
        'sale_by_type': sale_by_type,
        'sale_distribution': sale_distribution,
    }
    return render(request, 'sale_summary/detailed_crop_sale_summary.html', context)

def detailed_livestock_sale(request):
    sales = Sale.objects.filter(user=request.user).all()
    livestock_sales = []
    livestock_sales_names = []
    for sale in sales:
        if sale.category == 'livestock':
            livestock_sales.append(sale)
            livestock_sales_names.append(sale.product_name)
    product_types = []
    for name in livestock_sales_names:
        if name not in product_types:
            product_types.append(name)

    total_amount = sum(sale.total_amount for sale in livestock_sales)
    sale_by_type = [sales.filter(product_name=product_type).aggregate(total=models.Sum('total_amount'))['total'] or 0 for product_type in product_types]
    sale_distribution = [float(amount) / float(total_amount) * 100 if total_amount > 0 else 0 for amount in sale_by_type]
    print(product_types)
    print(sale_by_type)
    print(sale_distribution)
    context = {
        'livestock_sales': livestock_sales,
        'product_types': product_types,
        'sale_by_type': sale_by_type,
        'sale_distribution': sale_distribution,
    }
    return render(request, 'sale_summary/detailed_livestock_sale_summary.html', context)

def detailed_other_sale(request):
    sales = Sale.objects.filter(user=request.user).all()
    other_sales = []
    other_sales_names = []
    for sale in sales:
        if sale.category == 'other':
            other_sales.append(sale)
            other_sales_names.append(sale.product_name)
    product_types = []
    for name in other_sales_names:
        if name not in product_types:
            product_types.append(name)

    total_amount = sum(sale.total_amount for sale in other_sales)
    sale_by_type = [sales.filter(product_name=product_type).aggregate(total=models.Sum('total_amount'))['total'] or 0 for product_type in product_types]
    sale_distribution = [float(amount) / float(total_amount) * 100 if total_amount > 0 else 0 for amount in sale_by_type]
    print(product_types)
    print(sale_by_type)
    print(sale_distribution)
    context = {
        'other_sales': other_sales,
        'product_types': product_types,
        'sale_by_type': sale_by_type,
        'sale_distribution': sale_distribution,
    }
    return render(request, 'sale_summary/detailed_other_sale_summary.html', context)

# ***************************** A C C O U N T   M A N A G E M E N T *************************

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        try:
            user = User.objects.get(email=email, username=username)
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return redirect('password_reset_done')
            else:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'account_mgmt/forgot_password.html')
        except User.DoesNotExist:
            messages.error(request,  "User with this email and username does not exist.")
            return render(request, 'account_mgmt/forgot_password.html', )
    return render(request, 'account_mgmt/forgot_password.html')

class PasswordResetDoneView(TemplateView):
    template_name = 'account_mgmt/password_reset_done.html'

def account_details(request):
    user_details = User.objects.filter(id=request.user.id).all()
    return render(request, 'account_mgmt/account_details.html', {'user_details': user_details})

class EditAccountDetails(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditAccountDetailsForm
    template_name = 'account_mgmt/edit_account_details.html'
    success_url = reverse_lazy('account_details')

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.id)

class ChangePassword(PasswordChangeView):
    template_name = 'account_mgmt/change_password.html'
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDone(TemplateView):
    template_name = 'account_mgmt/password_change_done.html'

def delete_account(request):
    if request.method == 'POST':
        delete_form = DeleteAccountForm(request.POST)
        if request.user.is_authenticated:
            if delete_form.is_valid():
                request.user.delete()
                logout(request)
                return redirect('signup')
            return render(request, 'account_mgmt/delete_account.html', )
        return redirect('login')
    return render(request, 'account_mgmt/delete_account.html')

class AccountDeletionDone(TemplateView):
    template_name = 'account_mgmt/account_deletion_done.html'