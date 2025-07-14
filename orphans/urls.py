# orphans/urls.py

from django.urls import path
from .views import (
    upload_excel,
    orphan_list,
    orphan_add,
    orphan_edit,
    orphan_delete,
    orphan_details,
    add_sponsorship,
    archived_orphans,
    archived_sponsorships,
    export_orphans_to_csv
)

urlpatterns = [
    path('upload-excel/', upload_excel, name='upload_excel'),
    path('', orphan_list, name='orphan_list'),
    path('add/', orphan_add, name='orphan_add'),
    path('edit/<int:id>/', orphan_edit, name='orphan_edit'),
    path('delete/<int:id>/', orphan_delete, name='orphan_delete'),
    path('details/<int:id>/', orphan_details, name='orphan_details'),
    path('add-sponsorship/', add_sponsorship, name='add_sponsorship'),
    path('archived-orphans/', archived_orphans, name='archived_orphans'),
    path('archived-sponsorships/<int:orphan_id>/', archived_sponsorships, name='archived_sponsorships'),
    path('export/', export_orphans_to_csv, name='export_orphans_to_csv'),
]
