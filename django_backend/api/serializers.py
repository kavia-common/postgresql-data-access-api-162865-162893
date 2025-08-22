from rest_framework import serializers
from .models import Record

# PUBLIC_INTERFACE
class RecordSerializer(serializers.ModelSerializer):
    """Serializer for the Record model used to convert DB rows to JSON."""
    class Meta:
        model = Record
        fields = ('id', 'name', 'value', 'created_at')
