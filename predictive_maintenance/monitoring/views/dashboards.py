from django.shortcuts import render
from monitoring.models import Motor, Maintenance, LogActivity
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Max
from django.core.paginator import Paginator


@login_required(login_url='login')
def dashboard(request):
    motors = Motor.objects.all()
    maintenances = Maintenance.objects.all()
    users = User.objects.all()
    
    logs_list = LogActivity.objects.all().order_by('-timestamp')
    # Konfigurasi Pagination
    paginator = Paginator(logs_list, 4)
    page_number = request.GET.get('page')
    logs = paginator.get_page(page_number)

    # Hanya ambil motor yang memiliki maintenance (total_trend > 0)
    trends = motors.annotate(
        total_trend=Count('maintenance'),
        last_created=Max('maintenance__created_at')
    ).filter(total_trend__gt=0).order_by('-last_created')

    context = {
        'motors' : motors,
        'maintenances': maintenances,
        'users': users,
        'logs': logs,
        'trends': trends
    }
    return render(request, 'dashboard.html', context)