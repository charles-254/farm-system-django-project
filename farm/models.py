from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date


date_format_validator = RegexValidator(
    regex=r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD format
    message='Date must be in the format YYYY-MM-DD',
    code='invalid_date_format')

class Employee(models.Model):
    national_ID = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    salary = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_employed = models.DateField(validators=[date_format_validator], default=date.today(), blank=True)


    def __str__(self):
        return self.name

class PaymentStatus(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    unpaid_months = models.IntegerField(default='0')

    @property
    def salary(self):
        return self.employee.salary

    @property
    def name(self):
        return self.employee.name

    def __str__(self):
        return self.employee.name + "'s Payment Status"

class PaymentRecords(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payment_date = models.DateField(validators=[date_format_validator])
    salary = models.IntegerField(default=0)

class TotalAmountPaid(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, primary_key=True)
    total_amount = models.IntegerField(default=0)

class Crop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_id = models.AutoField(primary_key=True)
    crop_name = models.CharField(max_length=255)
    planting_date = models.DateField(default=date.today())
    harvested = models.BooleanField(default=False)
    harvesting_date = models.DateField(blank=True, null=True)
    yield_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.crop_name

class Livestock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    livestock_id = models.AutoField(primary_key=True)
    livestock_type = models.CharField(max_length=255)
    livestock_breed = models.CharField(max_length=255)
    quantity = models.IntegerField()
    health_status = models.CharField(max_length=255)
    notes = models.TextField()

    def __str__(self):
        return f"{self.livestock_type} - {self.livestock_breed}"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=300)
    date = models.DateField(default=date.today())
    achieved = models.BooleanField(default=False)
    achievement_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.date}"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=300)
    date = models.DateField(default=date.today())
    deadline = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(default=date.today())
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} - {self.date}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today())

    def __str__(self):
        return f"{self.expense_name} - {self.date}"