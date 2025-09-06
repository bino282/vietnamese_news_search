# Thiết Kế Hệ Thống Website Tìm Kiếm Tin Tức

## 1. Phân Tích Cấu Trúc Dữ Liệu

Dữ liệu tin tức có cấu trúc JSON với các trường:
- `id`: Mã định danh bài báo (int)
- `author`: Tác giả (string, có thể rỗng)
- `content`: Nội dung bài báo (string) - **Trường chính để tìm kiếm**
- `picture_count`: Số lượng hình ảnh (int)
- `processed`: Trạng thái xử lý (int)
- `source`: Nguồn tin (string) - VD: "docbao.vn"
- `title`: Tiêu đề bài báo (string) - **Trường quan trọng cho tìm kiếm**
- `topic`: Chủ đề (string) - VD: "Pháp luật"
- `url`: Đường dẫn gốc (string)
- `crawled_at`: Thời gian thu thập (string)

## 2. Kiến Trúc Hệ Thống

### Backend (Python Flask)
- **API Endpoint**: `/search` - Nhận query và trả về kết quả
- **TF-IDF Engine**: Xử lý tìm kiếm văn bản
- **Text Preprocessing**: Tiền xử lý văn bản tiếng Việt
- **Data Storage**: Lưu trữ dữ liệu JSON và index TF-IDF

### Frontend (HTML/CSS/JavaScript)
- **Search Interface**: Ô tìm kiếm và nút submit
- **Results Display**: Hiển thị danh sách kết quả
- **Responsive Design**: Tương thích mobile và desktop
- **Modern UI**: Giao diện đẹp, dễ sử dụng

## 3. Thuật Toán TF-IDF

### Term Frequency (TF)
- Tần suất xuất hiện của từ trong document
- TF(t,d) = (số lần từ t xuất hiện trong d) / (tổng số từ trong d)

### Inverse Document Frequency (IDF)
- Độ hiếm của từ trong toàn bộ corpus
- IDF(t) = log(N / df(t))
- N: tổng số documents, df(t): số documents chứa từ t

### TF-IDF Score
- TF-IDF(t,d) = TF(t,d) × IDF(t)

## 4. Xử Lý Văn Bản Tiếng Việt

### Tiền Xử Lý
- Loại bỏ dấu câu và ký tự đặc biệt
- Chuyển về chữ thường
- Tách từ (word segmentation) cho tiếng Việt
- Loại bỏ stop words tiếng Việt

### Tìm Kiếm
- Kết hợp tìm kiếm trên cả `title` và `content`
- Trọng số cao hơn cho `title`
- Sắp xếp kết quả theo điểm TF-IDF

## 5. Giao Diện Người Dùng

### Trang Chính
- Header với logo và tiêu đề
- Ô tìm kiếm trung tâm
- Footer với thông tin

### Trang Kết Quả
- Ô tìm kiếm ở trên
- Danh sách kết quả với:
  - Tiêu đề bài báo (link)
  - Đoạn trích nội dung
  - Nguồn và thời gian
  - Chủ đề
- Phân trang nếu có nhiều kết quả

