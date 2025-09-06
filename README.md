# Website Tìm Kiếm Tin Tức Việt Nam với TF-IDF

Đây là một hệ thống tìm kiếm tin tức Việt Nam hoàn chỉnh sử dụng thuật toán TF-IDF, được xây dựng với Python Flask backend và HTML/CSS/JavaScript frontend.

## 🌟 Tính Năng

- **Thuật toán TF-IDF**: Tìm kiếm chính xác với thuật toán TF-IDF được cài đặt từ đầu
- **Xử lý tiếng Việt**: Hỗ trợ tìm kiếm tiếng Việt với xử lý stop words và tokenization
- **Giao diện đẹp**: Frontend responsive với thiết kế hiện đại
- **API RESTful**: Backend Flask với các endpoint API đầy đủ
- **Dữ liệu mẫu**: Bao gồm 5 bài báo mẫu để test

## 📁 Cấu Trúc Dự Án

```
vietnamese_news_search/
├── news_search_api/           # Flask application chính
│   ├── src/
│   │   ├── main.py           # Entry point Flask app
│   │   ├── routes/
│   │   │   └── search.py     # API routes tìm kiếm
│   │   ├── static/           # Frontend files
│   │   │   ├── index.html    # Giao diện chính
│   │   │   ├── style.css     # CSS styling
│   │   │   └── script.js     # JavaScript logic
│   │   ├── basic_text_processor.py  # Text processor đơn giản
│   │   ├── simple_tfidf.py          # TF-IDF implementation thuần Python
│   │   └── text_processor.py       # Text processor với underthesea
│   ├── data/                 # Dữ liệu cho Flask app
│   └── requirements.txt      # Dependencies
└── system_design.md          # Thiết kế hệ thống
```

## 🚀 Cách Chạy

### 1. Cài Đặt Dependencies

```bash
cd vietnamese_news_search/news_search_api
pip install -r requirements.txt
```

### 2. Chạy Flask Server

```bash
python src/main.py
```

### 3. Truy Cập Website

Mở trình duyệt và truy cập: `http://localhost:5000`

## 🔧 Các Phiên Bản Implementation

### Phiên Bản Đơn Giản (src/simple_tfidf.py + src/basic_text_processor.py)
- TF-IDF implementation thuần Python
- Text processing cơ bản không cần external libraries
- Phù hợp cho deployment

## 🔍 Cách Sử Dụng

1. **Tìm kiếm**: Nhập từ khóa vào ô tìm kiếm
2. **Gợi ý**: Click vào các tag gợi ý để tìm kiếm nhanh
3. **Kết quả**: Xem danh sách kết quả với điểm số TF-IDF
4. **Chi tiết**: Click vào bài báo để xem link gốc

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Python 3.11**
- **Flask**: Web framework
- **TF-IDF**: Thuật toán tìm kiếm
- **underthesea**: Xử lý tiếng Việt (phiên bản đầy đủ)

### Frontend
- **HTML5**: Cấu trúc trang web
- **CSS3**: Styling với gradient và animations
- **JavaScript**: Logic tương tác
- **Responsive Design**: Tương thích mobile

## 📈 Hiệu Suất

- **Vocabulary Size**: 420 từ (với dữ liệu mẫu)
- **Documents**: 5 bài báo
- **Response Time**: < 100ms cho tìm kiếm
- **Accuracy**: Điểm TF-IDF từ 0-1

## 🔮 Mở Rộng

### Thêm Dữ Liệu
1. Cập nhật file `data/sample_news.json`
2. Restart server để rebuild index

### Tùy Chỉnh UI
1. Chỉnh sửa `src/static/style.css` cho giao diện
2. Cập nhật `src/static/script.js` cho logic

### API Endpoints
- `GET /api/health`: Health check
- `POST /api/search`: Tìm kiếm tin tức
- `GET /api/stats`: Thống kê hệ thống

## 📝 Ghi Chú

- Hệ thống sử dụng TF-IDF thuần Python để tương thích deployment
- Frontend responsive tương thích desktop và mobile
- Hỗ trợ CORS cho API calls
- Bao gồm error handling và loading states

