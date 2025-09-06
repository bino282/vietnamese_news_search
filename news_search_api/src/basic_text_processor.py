"""
Basic Vietnamese text processor without external dependencies
"""

import re
import string
from typing import List, Set

class BasicVietnameseTextProcessor:
    def __init__(self):
        # Danh sách stop words tiếng Việt cơ bản
        self.stop_words = {
            'và', 'của', 'có', 'là', 'được', 'cho', 'từ', 'với', 'trong', 'trên',
            'dưới', 'về', 'theo', 'như', 'để', 'khi', 'nếu', 'mà', 'hay', 'hoặc',
            'nhưng', 'vì', 'do', 'bởi', 'tại', 'qua', 'ra', 'vào', 'lên', 'xuống',
            'này', 'đó', 'kia', 'nào', 'đâu', 'sao', 'thế', 'thì', 'rồi', 'đã',
            'sẽ', 'đang', 'bị', 'phải', 'cần', 'nên', 'có thể', 'không', 'chưa',
            'vẫn', 'còn', 'đều', 'cũng', 'cả', 'mọi', 'nhiều', 'ít', 'một', 'hai',
            'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười', 'trăm', 'nghìn',
            'triệu', 'tỷ', 'lần', 'ngày', 'tháng', 'năm', 'giờ', 'phút', 'giây',
            'người', 'việc', 'điều', 'cách', 'lúc', 'chỗ', 'nơi', 'đây', 'đấy',
            'ở', 'tôi', 'bạn', 'anh', 'chị', 'em', 'ông', 'bà', 'cô', 'chú',
            'thầy', 'cô', 'các', 'những', 'mỗi', 'từng', 'ai', 'gì', 'đâu', 'nào'
        }
    
    def clean_text(self, text: str) -> str:
        """Làm sạch văn bản"""
        if not text:
            return ""
        
        # Chuyển về chữ thường
        text = text.lower()
        
        # Loại bỏ HTML tags nếu có
        text = re.sub(r'<[^>]+>', '', text)
        
        # Loại bỏ URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Loại bỏ email
        text = re.sub(r'\S+@\S+', '', text)
        
        # Loại bỏ số điện thoại
        text = re.sub(r'[\+]?[1-9]?[0-9]{7,15}', '', text)
        
        # Giữ lại chữ cái tiếng Việt, số và khoảng trắng
        text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text)
        
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def simple_tokenize(self, text: str) -> List[str]:
        """Tách từ đơn giản bằng khoảng trắng"""
        if not text:
            return []
        
        # Làm sạch văn bản trước
        clean_text = self.clean_text(text)
        
        # Tách từ bằng khoảng trắng
        tokens = clean_text.split()
        
        # Lọc bỏ stop words và từ có độ dài < 2
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stop_words and len(token) >= 2
        ]
        
        return filtered_tokens
    
    def preprocess_document(self, title: str, content: str) -> str:
        """Tiền xử lý document (kết hợp title và content)"""
        # Gán trọng số cao hơn cho title bằng cách lặp lại 2 lần
        title_tokens = self.simple_tokenize(title)
        content_tokens = self.simple_tokenize(content)
        
        # Kết hợp title (x2) và content
        all_tokens = title_tokens * 2 + content_tokens
        
        return ' '.join(all_tokens)
    
    def preprocess_query(self, query: str) -> str:
        """Tiền xử lý query tìm kiếm"""
        tokens = self.simple_tokenize(query)
        return ' '.join(tokens)

# Test module
if __name__ == "__main__":
    processor = BasicVietnameseTextProcessor()
    
    # Test với văn bản mẫu
    title = "Tên cướp tiệm vàng tại Huế là đại úy công an"
    content = "Theo thông tin từ Công an tỉnh Thừa Thiên Huế, đối tượng cướp tiệm vàng..."
    
    print("Original title:", title)
    print("Processed title:", processor.simple_tokenize(title))
    print()
    print("Original content:", content[:100] + "...")
    print("Processed content:", processor.simple_tokenize(content)[:10])
    print()
    print("Combined document:", processor.preprocess_document(title, content)[:100] + "...")

