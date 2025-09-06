"""
TF-IDF Search Engine cho hệ thống tìm kiếm tin tức tiếng Việt
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from text_processor import VietnameseTextProcessor

class TFIDFSearchEngine:
    def __init__(self):
        self.text_processor = VietnameseTextProcessor()
        self.vectorizer = TfidfVectorizer(
            max_features=10000,  # Giới hạn số features
            ngram_range=(1, 2),  # Sử dụng unigram và bigram
            min_df=1,           # Từ phải xuất hiện ít nhất 1 lần
            max_df=0.95         # Loại bỏ từ xuất hiện quá nhiều
        )
        self.tfidf_matrix = None
        self.documents = []
        self.processed_docs = []
    
    def load_data(self, json_file_path: str):
        """Tải dữ liệu từ file JSON"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
            print(f"Đã tải {len(self.documents)} documents")
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            self.documents = []
    
    def build_index(self):
        """Xây dựng index TF-IDF"""
        if not self.documents:
            print("Không có dữ liệu để xây dựng index")
            return
        
        print("Đang xử lý văn bản...")
        # Tiền xử lý tất cả documents
        self.processed_docs = []
        for doc in self.documents:
            processed_doc = self.text_processor.preprocess_document(
                doc.get('title', ''), 
                doc.get('content', '')
            )
            self.processed_docs.append(processed_doc)
        
        print("Đang tính toán TF-IDF matrix...")
        # Tính toán TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_docs)
        print(f"TF-IDF matrix shape: {self.tfidf_matrix.shape}")
        print("Hoàn thành xây dựng index!")
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[Dict, float]]:
        """Tìm kiếm documents liên quan đến query"""
        if self.tfidf_matrix is None:
            print("Index chưa được xây dựng. Vui lòng gọi build_index() trước.")
            return []
        
        # Tiền xử lý query
        processed_query = self.text_processor.preprocess_query(query)
        if not processed_query.strip():
            print("Query rỗng sau khi xử lý")
            return []
        
        # Chuyển query thành vector TF-IDF
        query_vector = self.vectorizer.transform([processed_query])
        
        # Tính cosine similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Sắp xếp theo độ tương đồng giảm dần
        ranked_indices = np.argsort(similarities)[::-1]
        
        # Lấy top_k kết quả có score > 0
        results = []
        for idx in ranked_indices[:top_k]:
            if similarities[idx] > 0:
                results.append((self.documents[idx], float(similarities[idx])))
        
        return results
    
    def get_stats(self) -> Dict:
        """Lấy thống kê về search engine"""
        if self.tfidf_matrix is None:
            return {"status": "Index chưa được xây dựng"}
        
        return {
            "total_documents": len(self.documents),
            "vocabulary_size": len(self.vectorizer.vocabulary_),
            "tfidf_matrix_shape": self.tfidf_matrix.shape,
            "sample_features": list(self.vectorizer.vocabulary_.keys())[:10]
        }

# Test search engine
if __name__ == "__main__":
    # Khởi tạo search engine
    search_engine = TFIDFSearchEngine()
    
    # Tải dữ liệu mẫu
    search_engine.load_data('../data/sample_news.json')
    
    # Xây dựng index
    search_engine.build_index()
    
    # Test tìm kiếm
    test_queries = [
        "cướp tiệm vàng",
        "chứng khoán VN-Index",
        "COVID-19 ca mắc",
        "bóng đá Việt Nam",
        "điểm chuẩn đại học"
    ]
    
    print("\n" + "="*50)
    print("TEST TÌM KIẾM")
    print("="*50)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = search_engine.search(query, top_k=3)
        
        if results:
            for i, (doc, score) in enumerate(results, 1):
                print(f"{i}. [{score:.3f}] {doc['title']}")
                print(f"   Topic: {doc['topic']} | Source: {doc['source']}")
        else:
            print("Không tìm thấy kết quả phù hợp")
    
    # Hiển thị thống kê
    print("\n" + "="*50)
    print("THỐNG KÊ SEARCH ENGINE")
    print("="*50)
    stats = search_engine.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

