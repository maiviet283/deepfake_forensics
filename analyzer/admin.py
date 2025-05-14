from django.contrib import admin
from .models import Image
from django.utils.html import format_html
# Register your models here.

class AdminImage(admin.ModelAdmin):
    list_display = ['id','name','result','probability','created_at','image_preview']
    list_per_page = 8
    search_fields = ['id','name','result','probability']
    list_filter = ['created_at','result','probability']

    def image_preview(self, obj):
            """Hiển thị ảnh image trong danh sách admin"""
            if obj.image:
                return format_html('<img src="{}" height="100" style="border-radius:5px;" />', obj.image.url)
            return "(Không có ảnh)"

    image_preview.short_description = "Ảnh đại diện"

admin.site.register(Image, AdminImage)