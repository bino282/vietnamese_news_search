"""
Search API routes cho hệ thống tìm kiếm tin tức
"""

from flask import Blueprint, request, jsonify
from src.simple_tfidf import SimpleTFIDFSearchEngine
import os

search_bp = Blueprint('search', __name__)

# Khởi tạo search engine global
search_engine = None

def init_search_engine():
    """Khởi tạo search engine"""
    global search_engine
    if search_engine is None:
        search_engine = SimpleTFIDFSearchEngine()
        # Đường dẫn tới file dữ liệu
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'sample_news.json')
        search_engine.load_data(data_path)
        search_engine.build_index()
        print("Search engine đã được khởi tạo!")

@search_bp.route('/search', methods=['GET', 'POST'])
def search_news():
    """API endpoint tìm kiếm tin tức"""
    try:
        # Search engine đã được khởi tạo từ main.py
        global search_engine
        if search_engine is None:
            return jsonify({
                'success': False,
                'message': 'Search engine chưa được khởi tạo',
                'results': []
            }), 500
        
        # Lấy query từ request
        if request.method == 'GET':
            query = request.args.get('q', '').strip()
            limit = int(request.args.get('limit', 10))
        else:  # POST
            data = request.get_json()
            query = data.get('query', '').strip() if data else ''
            limit = int(data.get('limit', 10)) if data else 10
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Query không được để trống',
                'results': []
            }), 400
        
        # Giới hạn số kết quả
        limit = min(max(limit, 1), 50)  # Từ 1 đến 50
        
        # Thực hiện tìm kiếm
        results = search_engine.search(query, top_k=limit)
        
        # Format kết quả
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'id': doc['id'],
                'title': doc['title'],
                'content': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content'],
                'author': doc['author'],
                'source': doc['source'],
                'topic': doc['topic'],
                'url': doc['url'],
                'crawled_at': doc['crawled_at'],
                'score': round(score, 4)
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'total_results': len(formatted_results),
            'results': formatted_results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}',
            'results': []
        }), 500

@search_bp.route('/stats', methods=['GET'])
def get_stats():
    """API endpoint lấy thống kê search engine"""
    try:
        global search_engine
        if search_engine is None:
            return jsonify({
                'success': False,
                'message': 'Search engine chưa được khởi tạo',
                'results': []
            }), 500
        
        stats = search_engine.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@search_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Search API đang hoạt động',
        'version': '1.0.0'
    })

