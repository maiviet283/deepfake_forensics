import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def analyze_image(image_path):
    """
    Phân tích ảnh để xác định real hay fake dựa trên một số yếu tố hình ảnh.
    
    :param image_path: Đường dẫn đến file ảnh cần phân tích
    :return: (label, ai_probability) -> "Real" hoặc "Fake" và xác suất %
    """
    try:
        # Đọc ảnh
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            return "Error", 0.0  # Trả về lỗi nếu không đọc được ảnh

        # Chuyển sang ảnh xám
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Tính độ sắc nét bằng Laplacian
        sharpness = cv2.Laplacian(gray_image, cv2.CV_64F).var()

        # Kiểm tra sự lặp lại của hình ảnh (chỉ số SSIM với ảnh làm mờ)
        blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 0)
        similarity = ssim(gray_image, blurred_image)

        # Kiểm tra mức độ nhiễu (càng nhiễu, càng có khả năng là AI tạo ra)
        noise = np.var(gray_image)

        # Xác định kết quả dựa trên mức độ nghi ngờ
        # Điều chỉnh hệ số tính toán AI probability
        ai_probability = min(max((similarity * 70) + (noise / 10) - (sharpness / 15), 0), 100)

        label = "Fake" if ai_probability > 50 else "Real"

        return label, round(ai_probability, 2)

    except Exception as e:
        print("Error:", str(e))
        return "Error", 0.0  # Nếu có lỗi, trả về trạng thái "Error"

# Ví dụ sử dụng
image_path = r"D:\IMAGES\BEA\4_47.jpg"
label, ai_probability = analyze_image(image_path)
print(f"Ảnh: {label}, Tỷ lệ AI: {ai_probability}%")
