from django.db import models
# from django.contrib.postgres.fields import JSONField 
from django.db.models import JSONField

class SERPResult(models.Model):
    task_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    fetched_data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task_id} - {self.username}'


class SERPTaskPostResult(models.Model):
    username = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    posted_data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task_id} - {self.username}'