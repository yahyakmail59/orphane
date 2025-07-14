# orphans/views.py

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Orphan, Sponsorship, ArchivedOrphan, ArchivedSponsorship
from .forms import OrphanForm, SponsorshipForm
from django.db.models import Q
import pandas as pd
from django.contrib import messages
from datetime import datetime
import csv

def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            messages.error(request, "يرجى اختيار ملف Excel لتحميله.")
            return redirect('orphan_list')

        try:
            df = pd.read_excel(excel_file)
            expected_columns = {'full_name', 'id_number', 'date_of_birth', 'guardian_name', 'guardian_id_number', 'guardian_phone'}
            if not expected_columns.issubset(df.columns):
                messages.error(request, "الملف يجب أن يحتوي على الأعمدة الصحيحة.")
                return redirect('orphan_list')

            for index, row in df.iterrows():
                Orphan.objects.create(
                    full_name=row['full_name'],
                    id_number=row['id_number'],
                    date_of_birth=row['date_of_birth'],
                    guardian_name=row['guardian_name'],
                    guardian_id_number=row['guardian_id_number'],
                    guardian_phone=row['guardian_phone']
                )

            messages.success(request, "تم تحميل البيانات بنجاح.")
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء تحميل الملف: {e}")

        return redirect('orphan_list')

def orphan_list(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    orphans = Orphan.objects.all()

    if query:
        orphans = orphans.filter(
            Q(full_name__icontains=query)
        )

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            orphans = orphans.filter(
                sponsorship__sponsorship_date__date__range=(start_date, end_date)
            ).distinct()
        except ValueError:
            messages.error(request, "تاريخ غير صالح.")
    
    return render(request, 'orphans/orphan_list.html', {'orphans': orphans})

def export_orphans_to_csv(request):
    # Fetch orphan data
    orphans = Orphan.objects.all().values('full_name', 'id_number', 'date_of_birth', 'guardian_name', 'guardian_id_number', 'guardian_phone')

    # Create a response object for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orphan-final.csv"'

    # Ensure correct encoding for Arabic text
    response.write('\ufeff'.encode('utf8'))

    # Create a CSV writer object with a semicolon as a delimiter
    writer = csv.writer(response, delimiter=';')

    # Write the header row
    writer.writerow(['الاسم الكامل', 'رقم الهوية', 'تاريخ الميلاد', 'اسم الوصي', 'رقم هوية الوصي', 'هاتف الوصي'])

    # Write orphan data rows
    for orphan in orphans:
        writer.writerow([
            orphan['full_name'],
            orphan['id_number'],
            orphan['date_of_birth'],
            orphan['guardian_name'],
            orphan['guardian_id_number'],
            orphan['guardian_phone']
        ])

    return response
def orphan_add(request):
    if request.method == 'POST':
        form = OrphanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('orphan_list')
    else:
        form = OrphanForm()
    return render(request, 'orphans/add_orphan.html', {'form': form})

def orphan_edit(request, id):
    orphan = get_object_or_404(Orphan, id=id)
    if request.method == 'POST':
        form = OrphanForm(request.POST, request.FILES, instance=orphan)
        if form.is_valid():
            form.save()
            return redirect('orphan_list')
    else:
        form = OrphanForm(instance=orphan)
    return render(request, 'orphans/orphan_form.html', {'form': form})

def orphan_delete(request, id):
    orphan = get_object_or_404(Orphan, id=id)
    if request.method == 'POST':
        # Archive orphan
        archived_orphan = ArchivedOrphan.objects.create(
            full_name=orphan.full_name,
            id_number=orphan.id_number,
            date_of_birth=orphan.date_of_birth,
            guardian_name=orphan.guardian_name,
            guardian_id_number=orphan.guardian_id_number,
            guardian_phone=orphan.guardian_phone,
            photo=orphan.photo
        )
        
        # Archive associated sponsorships
        sponsorships = Sponsorship.objects.filter(orphan=orphan)
        for sponsorship in sponsorships:
            ArchivedSponsorship.objects.create(
                orphan=archived_orphan,
                sponsorship_date=sponsorship.sponsorship_date,
                amount=sponsorship.amount
                # Add any other fields you need to archive
            )

        # Delete original orphan and its sponsorships
        orphan.delete()
        return redirect('orphan_list')
    return render(request, 'orphans/orphan_confirm_delete.html', {'orphan': orphan})


def orphan_details(request, id):
    orphan = get_object_or_404(Orphan, id=id)
    sponsorships = Sponsorship.objects.filter(orphan=orphan)
    return render(request, 'orphans/orphan_details.html', {
        'orphan': orphan,
        'sponsorships': sponsorships
    })

def add_sponsorship(request):
    if request.method == 'POST':
        form = SponsorshipForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form Data:", form.cleaned_data)  # Debugging print statement
            form.save()
            return redirect('add_sponsorship')
    else:
        form = SponsorshipForm()
    return render(request, 'orphans/add_sponsorship.html', {'form': form})

def archived_orphans(request):
    archived_orphans = ArchivedOrphan.objects.all()
    return render(request, 'orphans/archived_orphans.html', {'archived_orphans': archived_orphans})

def archived_sponsorships(request, orphan_id):
    archived_orphan = get_object_or_404(ArchivedOrphan, id=orphan_id)
    archived_sponsorships = ArchivedSponsorship.objects.filter(orphan=archived_orphan)
    return render(request, 'orphans/archived_sponsorships.html', {
        'archived_orphan': archived_orphan,
        'archived_sponsorships': archived_sponsorships
    })
