"""
Simple TF-IDF implementation without numpy/scikit-learn for deployment
"""

import json
import math
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
from src.basic_text_processor import BasicVietnameseTextProcessor

class SimpleTFIDFSearchEngine:
    def __init__(self):
        self.text_processor = BasicVietnameseTextProcessor()
        self.documents = []
        self.processed_docs = []
        self.vocabulary = set()
        self.idf_scores = {}
        self.tf_idf_matrix = []
    
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
            self.processed_docs.append(processed_doc.split())
            self.vocabulary.update(processed_doc.split())
        
        print("Đang tính toán IDF scores...")
        # Tính IDF cho mỗi từ
        self.idf_scores = {}
        total_docs = len(self.processed_docs)
        
        for word in self.vocabulary:
            # Đếm số documents chứa từ này
            doc_freq = sum(1 for doc in self.processed_docs if word in doc)
            # Tính IDF
            self.idf_scores[word] = math.log(total_docs / doc_freq) if doc_freq > 0 else 0
        
        print("Đang tính toán TF-IDF matrix...")
        # Tính TF-IDF cho mỗi document
        self.tf_idf_matrix = []
        for doc_tokens in self.processed_docs:
            doc_length = len(doc_tokens)
            tf_idf_vector = {}
            
            if doc_length > 0:
                # Đếm tần suất từ
                word_counts = Counter(doc_tokens)
                
                # Tính TF-IDF cho mỗi từ
                for word in word_counts:
                    tf = word_counts[word] / doc_length  # Term Frequency
                    idf = self.idf_scores.get(word, 0)   # Inverse Document Frequency
                    tf_idf_vector[word] = tf * idf
            
            self.tf_idf_matrix.append(tf_idf_vector)
        
        print(f"Hoàn thành xây dựng index! Vocabulary size: {len(self.vocabulary)}")
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Tính cosine similarity giữa 2 vectors"""
        # Tìm từ chung
        common_words = set(vec1.keys()) & set(vec2.keys())
        
        if not common_words:
            return 0.0
        
        # Tính dot product
        dot_product = sum(vec1[word] * vec2[word] for word in common_words)
        
        # Tính magnitude của mỗi vector
        mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[Dict, float]]:
        """Tìm kiếm documents liên quan đến query"""
        if not self.tf_idf_matrix:
            print("Index chưa được xây dựng. Vui lòng gọi build_index() trước.")
            return []
        
        # Tiền xử lý query
        processed_query = self.text_processor.preprocess_query(query)
        if not processed_query.strip():
            print("Query rỗng sau khi xử lý")
            return []
        
        query_tokens = processed_query.split()
        query_length = len(query_tokens)
        
        if query_length == 0:
            return []
        
        # Tạo TF-IDF vector cho query
        query_word_counts = Counter(query_tokens)
        query_vector = {}
        
        for word in query_word_counts:
            if word in self.vocabulary:
                tf = query_word_counts[word] / query_length
                idf = self.idf_scores.get(word, 0)
                query_vector[word] = tf * idf
        
        # Tính similarity với mỗi document
        similarities = []
        for i, doc_vector in enumerate(self.tf_idf_matrix):
            similarity = self.cosine_similarity(query_vector, doc_vector)
            similarities.append((i, similarity))
        
        # Sắp xếp theo độ tương đồng giảm dần
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Lấy top_k kết quả có score > 0
        results = []
        for doc_idx, score in similarities[:top_k]:
            if score > 0:
                results.append((self.documents[doc_idx], score))
        
        return results
    
    def get_stats(self) -> Dict:
        """Lấy thống kê về search engine"""
        if not self.tf_idf_matrix:
            return {"status": "Index chưa được xây dựng"}
        
        return {
            "total_documents": len(self.documents),
            "vocabulary_size": len(self.vocabulary),
            "sample_features": list(self.vocabulary)[:10] if self.vocabulary else []
        }

# Test simple search engine
if __name__ == "__main__":
    # Khởi tạo search engine
    search_engine = SimpleTFIDFSearchEngine()
    
    # Tải dữ liệu mẫu
    search_engine.load_data('../data/sample_news.json')
    
    # Xây dựng index
    search_engine.build_index()
    
    # Test tìm kiếm
    test_queries = [
        "cướp tiệm vàng",
        "chứng khoán VN-Index",
        "COVID-19 ca mắc"
    ]
    
    print("\n" + "="*50)
    print("TEST TÌM KIẾM SIMPLE TF-IDF")
    print("="*50)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = search_engine.search(query, top_k=2)
        
        if results:
            for i, (doc, score) in enumerate(results, 1):
                print(f"{i}. [{score:.3f}] {doc['title']}")
        else:
            print("Không tìm thấy kết quả phù hợp")

