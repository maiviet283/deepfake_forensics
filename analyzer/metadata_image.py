import os
import magic
from PIL import Image
from datetime import datetime

def get_image_metadata(filepath):
    metadata = {}

    try:
        stat_info = os.stat(filepath)
        metadata.update({
            'created_time': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified_time': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'file_size': f"{round(stat_info.st_size / 1024, 2)} KB"
        })
    except Exception as e:
        metadata['error_system_info'] = str(e)

    try:
        metadata['mime_type'] = magic.from_file(filepath, mime=True)
    except Exception as e:
        metadata['mime_type'] = f'Unknown ({str(e)})'

    try:
        with Image.open(filepath) as img:
            metadata.update({
                'image_format': img.format,
                'dimensions': f"{img.width} x {img.height}"
            })
    except Exception as e:
        metadata.update({'image_format': 'Cannot open', 'error_image': str(e)})

    return metadata
