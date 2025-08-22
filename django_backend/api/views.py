from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Record
from .serializers import RecordSerializer


@api_view(['GET'])
def health(request):
    """
    Health check endpoint.
    Returns 200 OK when the service is running.
    """
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method='get',
    operation_id='records_list',
    operation_summary='List all records',
    operation_description='Returns all rows from the PostgreSQL "Record" table as JSON.',
    responses={
        200: openapi.Response('List of records', RecordSerializer(many=True)),
        500: 'Server Error',
    },
    tags=['records'],
)
@api_view(['GET'])
def list_records(request):
    """Fetch and return all rows from the Record table."""
    try:
        queryset = Record.objects.all().order_by('id')
        serializer = RecordSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as exc:
        return Response(
            {"detail": f"Failed to retrieve records: {exc}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
