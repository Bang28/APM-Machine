from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Motor(models.Model):
    tag_number = models.CharField(_("Tag No"), max_length=50, unique=True)
    name = models.CharField(_("Motor Name"), max_length=100, null=True, blank=True)
    # specification
    output = models.FloatField(_("Output"), help_text='Daya dalam KW', null=True, blank=True)
    voltage = models.FloatField(_("Voltage"), help_text='Tegangan dalam Volt', null=True, blank=True)
    starter_type = models.CharField(_("Starter Type"), max_length=50, null=True, blank=True)
    set_ol = models.FloatField(_("SET OL"), null=True, blank=True)
    input = models.FloatField(_("Input"), help_text='Arus dalam Ampere', null=True, blank=True)
    speed = models.FloatField(_("Speed"), help_text='RPM', null=True, blank=True)
    frek = models.FloatField(_("FREK/WEN/CY/HZ"), null=True, blank=True)
    frame = models.CharField(_("Frame"), max_length=50, null=True, blank=True)
    foundation_type = models.CharField(_("Fondation Type"), max_length=50, help_text='Rigid atau Flexible', null=True, blank=True)
    class_type = models.CharField(_("Class Type"), max_length=50, help_text='Kelas 2 atau 3', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")

    def __str__(self):
        return f"{self.name} - {self.tag_number}"
    
    class Meta:
        verbose_name = "Motor"
        verbose_name_plural = "Daftar Motor"


class Maintenance(models.Model):
    motor = models.ForeignKey("Motor", on_delete=models.CASCADE, verbose_name="Motor yang Dimaintenance")
    periodik = models.CharField(max_length=100, verbose_name="Periodik Maintenance") 
    tanggal_maintenance = models.DateField(verbose_name="Tanggal Maintenance", auto_now_add=True)
    keterangan = models.TextField(verbose_name="Keterangan", blank=True, null=True)
    pelaksana = models.CharField(max_length=100, verbose_name="Pelaksana", blank=True, null=True)
    
    # Menyimpan waktu pembuatan dan pembaruan data
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui Pada")

    def __str__(self):
        return f"{self.motor.name} - {self.periodik} - {self.tanggal_maintenance}"
    
    class Meta:
        verbose_name = "Perawatan Motor"
        verbose_name_plural = "Data Perawatan Motor"
    

class Measurement(models.Model):
    motor = models.ForeignKey(Motor, verbose_name=_("Motor"), on_delete=models.CASCADE)
    maintenance = models.OneToOneField(Maintenance, on_delete=models.CASCADE, verbose_name="Perawatan")
    date = models.DateField(_("Tanggal dibuat"), auto_now_add=True)
    # load current
    load_current_r = models.FloatField(_("Load Current R"), help_text='Arus dalam Ampere', null=True, blank=True)
    load_current_s = models.FloatField(_("Load Current S"), help_text='Arus dalam Ampere', null=True, blank=True)
    load_current_t = models.FloatField(_("Load Current T"), help_text='Arus dalam Ampere', null=True, blank=True)
    # bearing & coil temp
    bearing_temp_de = models.FloatField(_("Bearing D.E"), help_text='Maksimal 80°', null=True, blank=True)
    bearing_temp_nde = models.FloatField(_("Bearing N.D.E"), help_text='Maksimal 80°', null=True, blank=True)
    coil_temp = models.FloatField(_("Coil Temp"), help_text='Maksimal 80°', null=True, blank=True)

    def __str__(self):
        return f"{self.motor.name} - {self.date}"

    class Meta:
        verbose_name = "Pengukuran Motor"
        verbose_name_plural = "Data Pengukuran Motor"


class Vibration(models.Model):
    motor = models.ForeignKey(Motor, verbose_name=_("Motor"), on_delete=models.CASCADE)
    maintenance = models.OneToOneField(Maintenance, on_delete=models.CASCADE, verbose_name="Perawatan")
    date = models.DateField(_("Tanggal dibuat"), auto_now_add=True)
    # vibration motor (fondation)
    vib_rigid_de = models.FloatField(_("Rigid D.E"), help_text='Maksimal 4,5 mm/s', null=True, blank=True)
    vib_rigid_nde = models.FloatField(_("Rigid N.D.E"), help_text='Maksimal 4,5 mm/s', null=True, blank=True)
    vib_flexible_de = models.FloatField(_("Flexible D.E"), help_text='Maksimal 7,1 mm/s', null=True, blank=True)
    vib_flexible_nde = models.FloatField(_("Flexible N.D.E"), help_text='Maksimal 7,1 mm/s', null=True, blank=True)
    # vibration bearing
    vib_class_2_de = models.FloatField(_("Class 2 D.E"), help_text='Maksimal 4gE', null=True, blank=True)
    vib_class_2_nde = models.FloatField(_("Class 2 N.D.E"), help_text='Maksimal 4gE', null=True, blank=True)
    vib_class_3_de = models.FloatField(_("Class 3 D.E"), help_text='Maksimal 10gE', null=True, blank=True)
    vib_class_3_nde = models.FloatField(_("Class 3 N.D.E"), help_text='Maksimal 10gE', null=True, blank=True)

    def __str__(self):
        return f"{self.motor.name} - {self.class_type} - {self.date}"
    
    class Meta:
        verbose_name = "Getaran Motor"
        verbose_name_plural = "Data Getaran Motor"
    

class LogActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    action = models.CharField(max_length=100)  
    description = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

    class Meta:
        verbose_name = "Logs Activity"
        verbose_name_plural = "Logs Aktifitas Pengguna"

