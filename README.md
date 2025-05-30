# 🧠 AI Image Analyzer

**Phát hiện hình ảnh được tạo bằng trí tuệ nhân tạo (AI) nhanh chóng và chính xác.**

![AI Image Analyzer Logo](/media/result_demo/result_demo_1.png)

---

## 🌟 Thông Tin Dự Án

- 🔧 **Backend:** Django Framework  
- 🎨 **Giao diện Admin:** Jazzmin UI  
- 🧪 **Xử lý ảnh:** Gửi ảnh đến API của Decopy AI và Wasit AI để phân tích  
- 📊 **Phân tích kết quả:** Tổng hợp xác suất từ nhiều nguồn AI để đưa ra đánh giá chính xác  

---

## 🚀 Tính năng chính

- Upload và phân tích hình ảnh để xác định ảnh thật hay ảnh được tạo bằng AI  
- Hiển thị kết quả chi tiết kèm xác suất nhận diện  
- Lưu lịch sử phân tích ảnh, cho phép xem lại và xóa ảnh đã phân tích  
- Giao diện quản trị dễ dùng với Jazzmin UI  
- Tích hợp API bên ngoài (Decopy AI, Wasit AI) để nâng cao độ chính xác phân tích  

---

## ⚙️ Cài đặt và khởi chạy

1. **Clone dự án:**

    ```bash
    git clone https://github.com/maiviet283/deepfake_forensics.git
    cd deepfake_forensics
    ```

2. **Tạo và kích hoạt môi trường ảo:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3. **Cài đặt các dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Thiết lập database và migrate:**

    ```bash
    python manage.py migrate
    ```

5. **Chạy server phát triển:**

    ```bash
    python manage.py runserver
    ```

6. **Truy cập ứng dụng:**

    - Trang chủ: [http://localhost:8000/](http://localhost:8000/)  
    - Phân tích ảnh: [http://localhost:8000/analyzer/](http://localhost:8000/analyzer/)  
    - Lịch sử phân tích: [http://localhost:8000/analyzer/history/](http://localhost:8000/analyzer/history/)  
    - Trang quản trị admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 📄 Sử dụng

- Tải lên ảnh cần phân tích tại trang `/analyzer`  
- Kết quả trả về sẽ hiển thị mức độ ảnh có khả năng là ảnh AI hoặc ảnh thật kèm xác suất  
- Xem lại toàn bộ ảnh đã phân tích tại `/analyzer/history` và có thể xóa từng ảnh nếu cần  
- Quản trị hệ thống qua giao diện `/admin` với Jazzmin UI