![image](https://github.com/user-attachments/assets/d12208e4-ecc8-4cde-936a-2d2cb7c9f6e2)

- Giới thiệu chương trình
Đây là một ứng dụng web đơn giản sử dụng Python (Flask) cho phép người dùng:
Ký số một file bất kỳ bằng RSA.
Tạo file JSON chứa chữ ký số và public key.
Xác minh tính toàn vẹn và xác thực của file với chữ ký số và public key tương ứng.
Ứng dụng phù hợp cho việc học tập, thực hành các khái niệm liên quan đến mã hóa bất đối xứng, chữ ký số, và bảo mật dữ liệu.

- Các chức năng chính
1. Giao diện người gửi (/)
Gửi lên một file và hệ thống sẽ:
Sinh cặp khóa RSA (2048-bit).
Tạo chữ ký số SHA-256 với khóa riêng.
Tạo file JSON chứa: tên file, chữ ký (Base64) và public key (Base64).
Cho phép tải file JSON chứa chữ ký.
2. Giao diện người nhận (/receiver)
Cho phép người dùng tải lên file + nhập chữ ký và public key để:
Xác minh tính hợp lệ của chữ ký.
Thông báo kết quả xác minh (hợp lệ hoặc không).

- Cách hoạt động
Người gửi:
Upload file.
Server tạo khóa RSA và ký số nội dung.
Server trả lại JSON chứa chữ ký và public key.
Người nhận:
Upload lại file + cung cấp chữ ký và public key từ JSON.
Server xác minh chữ ký.

- Công nghệ sử dụng
Ngôn ngữ lập trình: Python 3.x
Web framework: Flask
Thư viện mã hóa: cryptography
Giao diện: HTML (thông qua render_template)
Lưu trữ file: hệ thống tệp và thư mục uploads/
Mã hóa và xác thực:
RSA 2048-bit
SHA-256
PKCS1v15 padding

