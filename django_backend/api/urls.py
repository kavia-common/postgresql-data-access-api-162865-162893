from django.urls import path
from .views import health, list_records

urlpatterns = [
    path('health/', health, name='Health'),
    path('records/', list_records, name='RecordsList'),
]
