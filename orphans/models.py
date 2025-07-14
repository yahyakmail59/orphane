from django.db import models
from datetime import datetime
from django.utils import timezone
class Orphan(models.Model):
    full_name = models.CharField('الإسم رباعي',max_length=255)
    id_number = models.CharField('رقم الهوية',max_length=20)
    date_of_birth = models.DateField('تاريخ الميلاد',)
    guardian_name = models.CharField('اسم الوصي',max_length=255)
    guardian_id_number = models.CharField('هوية الوصي',max_length=20)
    guardian_phone = models.CharField('جوال الوصي',max_length=30)
    photo = models.ImageField(upload_to='orphan_photos/',verbose_name='صورة اليتيم', blank=True, null=True)

    def __str__(self):
        return self.full_name

class Sponsorship(models.Model):
    orphan = models.ForeignKey(Orphan, on_delete=models.CASCADE,verbose_name='اختر يتيم')
    sponsor_name = models.CharField('اسم الجهة الكافلة',max_length=255)
    sponsorship_date = models.DateTimeField('تاريخ الكفالة',default=datetime.now)
    amount = models.DecimalField('قيمة الكفالة',max_digits=10, decimal_places=2, default=313.5)
    receipt_image = models.ImageField('صورة الإستلام للكفالة',upload_to='sponsorship_receipts/', null=True, blank=True)

    def __str__(self):
        return f"Sponsorship for {self.orphan.full_name} by {self.sponsor_name}"

class ArchivedOrphan(models.Model):
    full_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=255)
    guardian_id_number = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='archived_orphan_photos/', null=True, blank=True)
    archived_at = models.DateTimeField(default=timezone.now)

class ArchivedSponsorship(models.Model):
    orphan = models.ForeignKey(ArchivedOrphan, on_delete=models.CASCADE)
    sponsor_name = models.CharField('اسم الجهة الكافلة',max_length=255)
    sponsorship_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add any other fields from your Sponsorship model
