import os
import shutil
import smtplib
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import schedule

# Tải biến môi trường
load_dotenv()

# Định nghĩa thư mục
SOURCE_DIR = "database_folder"
BACKUP_DIR = "backup_folder"

# Kiểm tra và tạo thư mục nếu chưa tồn tại
if not os.path.exists(SOURCE_DIR):
    os.makedirs(SOURCE_DIR)
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def backup_va_thongbao():
    # Khởi tạo biến
    success = True
    message = []
    files_found = False
    
    # Sao chép file
    for file in os.listdir(SOURCE_DIR):
        if file.endswith(('.sql', '.sqlite3')):
            files_found = True
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = f"{os.path.splitext(file)[0]}_{timestamp}{os.path.splitext(file)[1]}"
                shutil.copy2(
                    os.path.join(SOURCE_DIR, file),
                    os.path.join(BACKUP_DIR, backup_filename)
                )
                message.append(f"Đã backup: {backup_filename}")
            except Exception as e:
                success = False
                message.append(f"Lỗi {file}: {str(e)}")
    
    # Nếu không tìm thấy file để backup
    if not files_found:
        message.append("Không tìm thấy file .sql hoặc .sqlite3 để backup.")

    # Gửi email thông báo
    sender = os.getenv('EMAIL_SENDER')
    receiver = os.getenv('EMAIL_RECIPIENT')
    subject = f"Backup {'Thành công' if success else 'Thất bại'} {datetime.now().strftime('%d/%m')}"
    body = '\n'.join(message)
    password = os.getenv('EMAIL_PASSWORD')
    
    # Tạo message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Thiết lập kết nối và gửi email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        print(f"Email đã được gửi đến {receiver}")
        server.quit()
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

if __name__ == "__main__":
    # Lập lịch chạy tự động lúc 0h mỗi ngày
    schedule.every().day.at("00:00").do(backup_va_thongbao)
    # backup_va_thongbao()
    print("Đang chạy dịch vụ backup...")
    
    # Vòng lặp để chạy lịch
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Dừng dịch vụ")
            