from django.db import models
from django.utils import timezone

class Image(models.Model):
    result_choices = (
        ('R','Ảnh Thật'),
        ('F','Ảnh Giả'),
        ('N','Chưa Xác Định')
    )

    name = models.CharField(max_length=128, default='AI Image Detector')
    image = models.ImageField(upload_to='image/%Y/%m/', blank=True, null=True)
    title = models.CharField(max_length=128, default='AI Image Detector')
    probability = models.FloatField(default=0) # xac suat %
    result = models.CharField(max_length=64, choices=result_choices, default='N')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_vietnam_time(self):
        """Trả về thời gian theo múi giờ Việt Nam"""
        return timezone.localtime(self.created_at, timezone.get_fixed_timezone(7))

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.result} - {self.probability}%'