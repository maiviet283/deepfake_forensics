import requests
import time

def detect_deepfake_from_image(image_path):
    """
    Gửi ảnh đến API decopy.ai để phân tích deepfake và trả về kết quả.
    
    :param image_path: Đường dẫn tới file ảnh cần phân tích
    :return: dict kết quả nếu thành công, hoặc None nếu thất bại
    """
    url_upload = "https://api.decopy.ai/api/decopy/ai-image-detector/create-job"

    try:
        with open(image_path, "rb") as f:
            files = {'image': (image_path.split('/')[-1], f, 'image/jpeg')}
            response = requests.post(url_upload, files=files)

        print("Upload status:", response.status_code)
        data = response.json()
        print("Upload response:", data)

        if data.get("code") == 100000:
            request_id = data["result"]["request_id"]
            url_result = f"https://api.decopy.ai/api/decopy/ai-image-detector/get-job/{request_id}"

            # Chờ server xử lý (có thể cần điều chỉnh thời gian)
            time.sleep(2)

            result_response = requests.get(url_result)
            print("Result status:", result_response.status_code)
            result_data = result_response.json()
            print("Detection result:", result_data)
            return result_data
        else:
            print("Upload failed.")
            return None
    except Exception as e:
        print("Error:", str(e))
        return None
