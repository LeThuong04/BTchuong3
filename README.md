# #💾Backup Script

Tự động sao lưu các file cơ sở dữ liệu và gửi email thông báo

##  Mục đích
- Tự động sao lưu file `.sql` và `.sqlite3` từ thư mục `database_folder` sang `backup_folder`
- Gửi email thông báo kết quả sao lưu
- Chạy tự động hàng ngày lúc 0h00

##  Cấu trúc thư mục

project_folder/
   database_folder/    # Chứa file cần backup (.sql, .sqlite3)
   backup_folder/     # Chứa file đã backup
   .env               # File chứa thông tin email
   backup.py          # File mã nguồn
   requirements.txt   # Danh sách thư viện cần thiết
   README.md          # File hướng dẫn


## 🛠 Yêu cầu hệ thống
- Python 3.6+
- Các thư viện cần thiết:
  ```bash
  python-dotenv
  schedule



##Cài đặt

Cài Python nếu chưa có: python.org.
Cài đặt các thư viện:pip install -r requirements.txt


Tạo file .env với nội dung:EMAIL_SENDER=your_email@gmail.com
EMAIL_RECIPIENT=recipient_email@example.com
EMAIL_PASSWORD=your_app_password


EMAIL_PASSWORD là App Password của Gmail (tạo tại Google Account > Security > App Passwords).



##Sử dụng

Đặt các file .sql hoặc .sqlite3 vào thư mục database_folder.
Chạy script:python backup.py


Script sẽ chạy backup lúc 0h mỗi ngày và gửi email thông báo.

##Kiểm tra ngay
Để chạy backup ngay lập tức, bỏ comment dòng # backup_va_thongbao() trong backup.py. Hoặc thay đổi lịch thành mỗi 10 giây:
schedule.every(10).seconds.do(backup_va_thongbao)

##Lưu ý

Đảm bảo file .env có thông tin đúng.
Kiểm tra kết nối mạng để gửi email.

