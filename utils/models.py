from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성시각')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시각')

    class Meta:
        abstract = True
