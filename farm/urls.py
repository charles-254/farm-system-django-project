from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='farm/login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('logout/', custom_logout, name='logout'),

    path('employee/', EmployeeView.as_view(), name='employee-view'),
    path('add-employee/', AddEmployee.as_view(), name='add-employee'),
    path('delete-employee/<int:pk>', DeleteEmployee.as_view(), name='delete-employee'),
    path('edit-employee/<int:pk>', EditEmployee.as_view(), name='edit-employee'),
    path('payment-status', EmployeePayment.as_view(), name='payment-status'),
    path('edit-unpaidmonths/<int:pk>', EditUnpaidMonths.as_view(), name='edit-unpaidmonths'),
    path('make-payments/<int:pk>', MakePayments.as_view(), name='make-payments'),
    path('payment-records', PaymentRecordsView.as_view(), name='payment-records'),

    path('crop_list', crop_list, name='crop_list'),
    path('add_crop', add_crop, name='add_crop'),
    path('edit_crop/<int:crop_id>/', edit_crop, name='edit_crop'),
    path('delete_crop/<int:pk>', DeleteCrop.as_view(), name='delete_crop'),
    path('harvest_crop/<int:crop_id>', harvest_crop, name='harvest_crop'),

    path('livestock_list', livestock_list, name='livestock_list'),
    path('add_livestock', add_livestock, name='add_livestock'),
    path('edit_livestock/<int:livestock_id>/', edit_livestock, name='edit_livestock'),
    path('delete_livestock/<int:pk>', DeleteLivestock.as_view(), name='delete_livestock'),

    path('goals/', goal_list, name='goal_list'),
    path('add_goal/', add_goal, name='add_goal'),
    path('edit_goal/<int:goal_id>/', edit_goal, name='edit_goal'),
    path('delete_goal/<int:pk>', DeleteGoal.as_view(), name='delete_goal'),
    path('achieve_goal/<int:goal_id>/', achieve_goal, name='achieve_goal'),
    path('active_goal/', active_goal, name='active_goal'),
    path('achieved_goal/', achieved_goal, name='achieved_goal'),

    path('tasks/', task_list, name='task_list'),
    path('add_task/', add_task, name='add_task'),
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'),
    path('delete_task/<int:pk>', DeleteTask.as_view(), name='delete_task'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('active_task/', active_task, name='active_task'),
    path('completed_task/', completed_task, name='completed_task'),

    path('sales/', sale_list, name='sale_list'),
    path('add_sale/', add_sale, name='add_sale'),
    path('edit_sale/<int:sale_id>/', edit_sale, name='edit_sale'),
    path('delete_sale/<int:pk>', DeleteSale.as_view(), name='delete_sale'),

    path('expenses/', expense_list, name='expense_list'),
    path('add_expense/', add_expense, name='add_expense'),
    path('edit_expense/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>', DeleteExpense.as_view(), name='delete_expense'),

    path('general_financial_report', financial_general_report, name='general_financial_report'),
    path('general_expense_summary', general_expense_summary, name='general_expense_summary'),
    path('expense_summary/detailed_crop_expense', detailed_crop_expense, name='detailed_crop_expense'),
    path('expense_summary/detailed_livestock_expense', detailed_livestock_expenses, name='detailed_livestock_expense'),
    path('expense_summary/detailed_other_expense', detailed_other_expense, name='detailed_other_expense'),

    path('general_sale_summary', general_sale_summary, name='general_sale_summary'),
    path('detailed_crop_sale', detailed_crop_sale, name='detailed_crop_sale'),
    path('detailed_livestock_sales', detailed_livestock_sale, name='detailed_livestock_sale'),
    path('detailed_other_sale', detailed_other_sale, name='detailed_other_sale'),

    path('forgot_password', forgot_password, name='forgot_password'),
    path('password_reset_done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account_details', account_details, name='account_details'),
    path('edit_account_details', EditAccountDetails.as_view(), name='edit_account_details'),
    path('change_password', ChangePassword.as_view(), name='change_password'),
    path('password_change_done', PasswordChangeDone.as_view(), name='password_change_done'),
    path('delete_account', delete_account, name='delete_account')

]
