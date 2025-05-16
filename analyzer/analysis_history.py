from .models import Image
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages


def get_history(request):
    analysis_history = Image.objects.all().order_by('-created_at')
    
    return render(request, 'analyzer/history.html',{
        'images': analysis_history
    })

def delete_history_by_id(request, id):
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=id)
        image.delete()
        messages.success(request, 'Xóa ảnh thành công.')
    else:
        messages.error(request, 'Yêu cầu không hợp lệ.')
    return redirect('analyzer:history')
