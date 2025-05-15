import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Image

@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    """Xóa file ảnh trong hệ thống khi bản ghi Image bị xóa"""
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
            print(f"Đã xóa ảnh: {instance.image.path}")
        except Exception as e:
            print(f"Lỗi khi xóa ảnh: {e}")
