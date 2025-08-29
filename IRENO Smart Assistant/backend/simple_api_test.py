"""
Final API Test - Test SOP Search API endpoint

This script creates a minimal Flask server and tests the SOP search functionality.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Import our modules
from azure_blob_handler import create_azure_blob_manager
from sop_search import keyword_search, search_with_highlights

app = Flask(__name__)
CORS(app)

# Initialize Azure manager
azure_manager = None
try:
    azure_manager = create_azure_blob_manager()
    print("✅ Azure Blob Manager initialized")
except Exception as e:
    print(f"❌ Azure initialization failed: {e}")

@app.route('/api/sop-search', methods=['POST'])
def sop_search():
    """SOP Document Search Endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Search query is required'}), 400
        
        search_query = data['query'].strip()
        
        if not search_query:
            return jsonify({'error': 'Search query cannot be empty'}), 400
        
        print(f"🔍 Searching for: '{search_query}'")
        
        if not azure_manager:
            return jsonify({
                'error': 'Azure Storage not configured',
                'query': search_query,
                'results': []
            }), 503
        
        try:
            # Get documents from Azure
            container_name = "sopdocuments"
            document_content = azure_manager.get_all_document_content(container_name)
            
            if not document_content:
                return jsonify({
                    'query': search_query,
                    'message': 'No SOP documents found',
                    'results': [],
                    'total_found': 0
                })
            
            # Perform search
            search_type = data.get('search_type', 'basic')
            
            if search_type == 'advanced':
                search_results = search_with_highlights(search_query, document_content, 10)
                
                if search_results and isinstance(search_results[0], dict) and "message" in search_results[0]:
                    return jsonify({
                        'query': search_query,
                        'search_type': search_type,
                        'message': search_results[0]["message"],
                        'results': [],
                        'total_found': 0
                    })
                
                return jsonify({
                    'query': search_query,
                    'search_type': search_type,
                    'results': search_results,
                    'total_found': len(search_results),
                    'message': f'Found {len(search_results)} results'
                })
            
            else:  # basic search
                search_results = keyword_search(search_query, document_content)
                
                if (len(search_results) == 1 and 
                    ("No results found" in search_results[0] or "Please provide" in search_results[0])):
                    return jsonify({
                        'query': search_query,
                        'search_type': search_type,
                        'message': search_results[0],
                        'results': [],
                        'total_found': 0
                    })
                
                formatted_results = []
                for i, result in enumerate(search_results[:10]):
                    formatted_results.append({
                        'snippet': result,
                        'result_number': i + 1,
                        'match_type': 'keyword'
                    })
                
                return jsonify({
                    'query': search_query,
                    'search_type': search_type,
                    'results': formatted_results,
                    'total_found': len(search_results),
                    'message': f'Found {len(search_results)} results'
                })
                
        except Exception as e:
            print(f"❌ Search error: {e}")
            return jsonify({
                'error': 'Search operation failed',
                'message': str(e),
                'query': search_query,
                'results': []
            }), 500
            
    except Exception as e:
        print(f"❌ API error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'results': []
        }), 500

@app.route('/', methods=['GET'])
def health_check():
    """Health check"""
    azure_status = "connected" if azure_manager else "disconnected"
    return jsonify({
        'status': 'healthy',
        'service': 'IRENO SOP Search API',
        'azure_storage': azure_status,
        'endpoints': {
            'POST /api/sop-search': 'Search SOP documents'
        }
    })

if __name__ == '__main__':
    print("🚀 Starting IRENO SOP Search API Server")
    print("=" * 50)
    print("📡 Endpoints:")
    print("   GET  / - Health check")
    print("   POST /api/sop-search - Search SOP documents")
    print("=" * 50)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
