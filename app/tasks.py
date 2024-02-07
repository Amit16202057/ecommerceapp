from celery import shared_task
from django.db.models import Sum
from .models import Order, DailyData
from datetime import datetime, timedelta

@shared_task
def calculate_daily_revenue():
    # Calculate total revenue for the last 24 hours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    total_revenue = Order.objects.filter(created_at__gte=start_date, created_at__lte=end_date).aggregate(total=Sum('total_amount'))['total']

    # Save DailyData
    DailyData.objects.create(date=end_date.date(), total_orders=Order.objects.filter(created_at__date=end_date.date()).count(), total_sales=total_revenue or 0)
