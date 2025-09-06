"""
Module xử lý văn bản tiếng Việt cho hệ thống tìm kiếm tin tức
"""

import re
import string
from underthesea import word_tokenize
from typing import List, Set

class VietnameseTextProcessor:
    def __init__(self):
        # Danh sách stop words tiếng Việt
        self.stop_words = self._load_vietnamese_stop_words()
    
    def _load_vietnamese_stop_words(self) -> Set[str]:
        """Tải danh sách stop words tiếng Việt"""
        stop_words = {
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
        return stop_words
    
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
    
    def tokenize(self, text: str) -> List[str]:
        """Tách từ tiếng Việt"""
        if not text:
            return []
        
        # Làm sạch văn bản trước
        clean_text = self.clean_text(text)
        
        # Tách từ bằng underthesea
        tokens = word_tokenize(clean_text)
        
        # Lọc bỏ stop words và từ có độ dài < 2
        filtered_tokens = [
            token for token in tokens 
            if token not in self.stop_words and len(token) >= 2
        ]
        
        return filtered_tokens
    
    def preprocess_document(self, title: str, content: str) -> str:
        """Tiền xử lý document (kết hợp title và content)"""
        # Gán trọng số cao hơn cho title bằng cách lặp lại 2 lần
        title_tokens = self.tokenize(title)
        content_tokens = self.tokenize(content)
        
        # Kết hợp title (x2) và content
        all_tokens = title_tokens * 2 + content_tokens
        
        return ' '.join(all_tokens)
    
    def preprocess_query(self, query: str) -> str:
        """Tiền xử lý query tìm kiếm"""
        tokens = self.tokenize(query)
        return ' '.join(tokens)

# Test module
if __name__ == "__main__":
    processor = VietnameseTextProcessor()
    
    # Test với văn bản mẫu
    title = "Tên cướp tiệm vàng tại Huế là đại úy công an"
    content = "Theo thông tin từ Công an tỉnh Thừa Thiên Huế, đối tượng cướp tiệm vàng..."
    
    print("Original title:", title)
    print("Processed title:", processor.tokenize(title))
    print()
    print("Original content:", content[:100] + "...")
    print("Processed content:", processor.tokenize(content)[:10])
    print()
    print("Combined document:", processor.preprocess_document(title, content)[:100] + "...")

