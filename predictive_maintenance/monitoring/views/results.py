from django.shortcuts import render , redirect, get_object_or_404
from django.db.models import Count, Min, Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from monitoring.models import Motor, Maintenance, LogActivity, Measurement, Vibration
from itertools import zip_longest
import json


@login_required(login_url='login')
def data_results(request):
    motors = Motor.objects.annotate(
        total_maintenance=Count('maintenance'),
        first_maintenance=Min('maintenance__tanggal_maintenance'),
        last_maintenance=Max('maintenance__created_at')
    ).filter(total_maintenance__gt=0).order_by('-last_maintenance')

    context = {
        'motors': motors
    }
    return render(request, 'tables/data_hasil.html', context)

@login_required(login_url='login')
def del_all_data_maintenance(request, motor_id):
    if request.method == "POST":
        motor = get_object_or_404(Motor, id=motor_id)

        # Cek apakah motor memiliki data maintenance
        maintenance_count = Maintenance.objects.filter(motor=motor).count()
        if maintenance_count == 0:
            messages.warning(request, f"Motor [{motor.tag_number}] belum memiliki data maintenance.")
            return redirect('data_results')
        
        # Hapus semua data maintenance terkait motor ini
        Maintenance.objects.filter(motor=motor).delete()
        
        # Simpan log aktivitas
        LogActivity.objects.create(
            user=request.user,
            action="Delete",
            description=f"Hapus semua data maintenance motor - Kode Motor : [{motor.tag_number}]."
        )

        messages.success(request, f"Semua data maintenance untuk motor [{motor.tag_number}] berhasil dihapus!")

    return redirect('data_results') 

@login_required(login_url='login')
def motor_trend(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)

    # Ambil Data Maintenance, Measurement, dan Vibration
    maintenances = list(Maintenance.objects.filter(motor=motor).order_by('-tanggal_maintenance')[:7])
    measurements = list(Measurement.objects.filter(motor=motor).order_by('-date')[:7])
    vibration_qs = Vibration.objects.filter(motor=motor).order_by('-date')[:7]  # Tetap QuerySet

    # Pastikan ada data getaran sebelum mengaksesnya
    if not vibration_qs.exists():  
        vibrations = []
    else:
        vibrations = list(vibration_qs)  # Baru dikonversi ke list setelah pengecekan

    # Pastikan jumlah data sama untuk zip_longest
    max_length = max(len(measurements), len(vibrations), len(maintenances))
    measurements += [None] * (max_length - len(measurements))
    vibrations += [None] * (max_length - len(vibrations))
    maintenances += [None] * (max_length - len(maintenances))

    # Buat trend data
    trend_data = list(zip_longest(measurements, vibrations, maintenances, fillvalue=None))

    # Load Current Data untuk Chart
    nominal_value = motor.input  # Nilai I. Nominal tetap
    load_current_data = {
        "dates": [m.date.strftime('%d-%m-%Y') for m in measurements if m],
        "R": [m.load_current_r for m in measurements if m],
        "S": [m.load_current_s for m in measurements if m],
        "T": [m.load_current_t for m in measurements if m],
        "Nominal": [nominal_value] * len(measurements),
    }

    # Bearing & Coil Temp Data
    temp_data = {
        "dates": [m.date.strftime('%d-%m-%Y') for m in measurements if m],
        "DE": [m.bearing_temp_de for m in measurements if m],
        "NDE": [m.bearing_temp_nde for m in measurements if m],
        "Coil": [m.coil_temp for m in measurements if m],
        "MaxTemp": [80] * len(measurements),
    }

    # Tentukan batas maksimum vibration motor berdasarkan type foundation
    max_vibration_motor = 4.5 if motor.foundation_type == "Rigid" else 7.1 if motor.foundation_type == "Flexible" else None

    # Vibration Motor Foundation (Rigid/Flexible)
    vib_found_data = {
        "dates": [v.date.strftime('%d-%m-%Y') for v in vibrations if v],
        "Rigid DE": [v.vib_rigid_de for v in vibrations if v],
        "Rigid NDE": [v.vib_rigid_nde for v in vibrations if v],
        "Flexible DE": [v.vib_flexible_de for v in vibrations if v],
        "Flexible NDE": [v.vib_flexible_nde for v in vibrations if v],
        "Max Vibration": [max_vibration_motor] * len(vibrations) if max_vibration_motor else [],
    }


    # Tentukan batas maksimum vibration bearing berdasarkan kelas motor
    max_vibration_bearing = 4 if motor.class_type == "Class 2" else 10 if motor.class_type == "Class 3" else None

    # Vibration Bearing Class Data
    vib_class_data = {
        "dates": [v.date.strftime('%d-%m-%Y') for v in vibrations if v],
        "Class 2 DE": [v.vib_class_2_de for v in vibrations if v],
        "Class 2 NDE": [v.vib_class_2_nde for v in vibrations if v],
        "Class 3 DE": [v.vib_class_3_de for v in vibrations if v],
        "Class 3 NDE": [v.vib_class_3_nde for v in vibrations if v],
        "Max Vibration": [max_vibration_bearing] * len(vibrations) if max_vibration_bearing else [],
    }

    context = {
        "motor": motor,
        "trend_data": trend_data,
        "load_current_data": json.dumps(load_current_data),
        "temp_data": json.dumps(temp_data),
        "vib_found_data": json.dumps(vib_found_data),
        "vib_class_data": json.dumps(vib_class_data),
    }

    return render(request, "tables/motor_trend.html", context)