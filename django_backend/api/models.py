from django.db import models


class Record(models.Model):
    """
    Record represents a simple table with name and value fields.
    Intended as an example of reading rows from PostgreSQL.
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.value})"
