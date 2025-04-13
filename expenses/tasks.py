import csv
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib.auth import get_user_model
from io import StringIO
from datetime import timedelta
from .models import Expense
import logging

logger = logging.getLogger(__name__)

def generate_monthly_expense_report():
    """
    Generate a monthly expense report for all users and send it by email.
    This can be scheduled with Django-crontab or Celery.
    """
    logger.info("Starting monthly expense report generation")
    
    User = get_user_model()
    users = User.objects.all()
    
    # Get the first day of previous month
    today = timezone.now()
    first_day = today.replace(day=1)
    last_month = first_day - timedelta(days=1)
    start_date = last_month.replace(day=1)
    
    for user in users:
        # Get expenses for the previous month
        expenses = Expense.objects.filter(
            user=user,
            created_at__gte=start_date,
            created_at__lt=first_day
        ).order_by('category', 'created_at')
        
        if not expenses:
            logger.info(f"No expenses found for user {user.username} in the last month")
            continue
            
        # Create CSV file
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(['Category', 'Description', 'Amount', 'Date'])
        
        total_amount = 0
        for expense in expenses:
            writer.writerow([
                expense.category,
                expense.description,
                str(expense.amount),
                expense.created_at.strftime('%Y-%m-%d')
            ])
            total_amount += expense.amount
            
        writer.writerow(['', 'Total', str(total_amount), ''])
        
        # Send email with report
        subject = f'Expense Report for {last_month.strftime("%B %Y")}'
        message = f'Please find attached your expense report for {last_month.strftime("%B %Y")}.'
        email = EmailMessage(
            subject,
            message,
            'expenses@yourcompany.com',
            [user.email],
        )
        email.attach(
            f'expense_report_{last_month.strftime("%Y_%m")}.csv',
            csv_buffer.getvalue(),
            'text/csv'
        )
        
        try:
            email.send()
            logger.info(f"Expense report sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send expense report to {user.email}: {str(e)}")
            
    logger.info("Monthly expense report generation completed")