from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    keyword = models.CharField(max_length=100)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.keyword

