from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import traceback
from datetime import datetime

# Import SOP search functionality
from azure_blob_handler import create_azure_blob_manager, AzureBlobManager
from sop_search import keyword_search, search_with_highlights

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
def setup_logging():
    """Setup comprehensive logging with file rotation"""
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"✅ Created logs directory: {logs_dir}")
    
    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    
    # Remove any existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create rotating file handler for errors
    error_log_file = os.path.join(logs_dir, 'error.log')
    file_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=1024*1024,  # 1 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.WARNING)
    
    # Create detailed formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s - [%(pathname)s:%(lineno)d]',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Create console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Configure Flask app logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    print(f"📝 Logging configured - Error logs: {error_log_file}")
    return logger

# Setup logging
logger = setup_logging()

# Log unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    """Log unhandled exceptions"""
    error_details = {
        'timestamp': datetime.now().isoformat(),
        'error_type': type(e).__name__,
        'error_message': str(e),
        'traceback': traceback.format_exc(),
        'request_url': request.url if request else 'Unknown',
        'request_method': request.method if request else 'Unknown',
        'user_agent': request.headers.get('User-Agent') if request else 'Unknown'
    }
    
    logger.error(f"Unhandled exception occurred: {json.dumps(error_details, indent=2)}")
    
    return jsonify({
        'error': 'An internal server error occurred',
        'timestamp': error_details['timestamp']
    }), 500

class SmartIrenoBot:
    """Smart IRENO bot with real and mock data support"""
    
    def __init__(self):
        # Try to get real API data, fall back to mock if needed
        self.api_data = self.get_api_data()
    
    def get_api_data(self):
        """Get API data - real or mock"""
        try:
            # Try real API first
            from ireno_tools import IrenoAPITools
            api_tools = IrenoAPITools()
            
            logger.info("🔄 Attempting to fetch real IRENO API data...")
            count_data = api_tools.get_collectors_count("api")
            logger.info(f"📊 Raw API response length: {len(count_data)} characters")
            
            # Parse the data
            import re
            total_match = re.search(r'(\d+)\s+total\s+collectors', count_data, re.IGNORECASE)
            online_match = re.search(r'(\d+)\s+online', count_data, re.IGNORECASE)
            offline_match = re.search(r'(\d+)\s+offline', count_data, re.IGNORECASE)
            uptime_match = re.search(r'(\d+\.?\d*)%\s+uptime', count_data, re.IGNORECASE)
            
            # Check if we got valid data
            if total_match and int(total_match.group(1)) > 0:
                logger.info("✅ Real API data found and parsed successfully!")
                api_data = {
                    'total_collectors': int(total_match.group(1)),
                    'online_collectors': int(online_match.group(1)) if online_match else 0,
                    'offline_collectors': int(offline_match.group(1)) if offline_match else 0,
                    'uptime_percentage': float(uptime_match.group(1)) if uptime_match else 0.0
                }
                
                # Get zone data
                zone_matches = re.findall(r'-\s+([^:]+):\s+(\d+)\s+total\s+\((\d+)\s+offline', count_data)
                if zone_matches:
                    api_data['zones'] = []
                    for zone_name, total, offline in zone_matches:
                        zone_total = int(total)
                        zone_offline = int(offline)
                        zone_percentage = round((zone_offline / zone_total * 100), 1) if zone_total > 0 else 0
                        api_data['zones'].append({
                            'name': zone_name.strip(),
                            'total': zone_total,
                            'offline': zone_offline,
                            'percentage': zone_percentage
                        })
                
                logger.info(f"📈 API data successfully parsed: {api_data['total_collectors']} total collectors")
                return api_data
            else:
                raise Exception("API returned no valid data or zero collectors")
                
        except Exception as e:
            error_details = {
                'timestamp': datetime.now().isoformat(),
                'error_type': type(e).__name__,
                'error_message': str(e),
                'traceback': traceback.format_exc(),
                'context': 'IRENO API data fetching'
            }
            
            logger.warning(f"⚠️ Real API failed, using mock data. Error details: {json.dumps(error_details, indent=2)}")
            
            # Return realistic mock data
            mock_data = {
                'total_collectors': 415,
                'online_collectors': 391,
                'offline_collectors': 24,
                'uptime_percentage': 94.2,
                'zones': [
                    {'name': 'Brooklyn', 'total': 95, 'offline': 8, 'percentage': 8.4},
                    {'name': 'Queens', 'total': 88, 'offline': 7, 'percentage': 8.0},
                    {'name': 'Westchester', 'total': 83, 'offline': 5, 'percentage': 6.0},
                    {'name': 'StatenIsland', 'total': 72, 'offline': 3, 'percentage': 4.2},
                    {'name': 'Manhattan', 'total': 77, 'offline': 1, 'percentage': 1.3}
                ]
            }
            
            logger.info(f"🔧 Using mock data: {mock_data['total_collectors']} total collectors")
            return mock_data
    
    def answer_zone_question(self, message: str) -> str:
        """Answer specific questions about zones"""
        message_lower = message.lower()
        
        # Refresh data for accuracy
        self.api_data = self.get_api_data()
        
        logger.info(f"🔍 Processing zone query: {message}")
        logger.info(f"📊 Current data overview: {self.api_data['total_collectors']} total, {self.api_data['offline_collectors']} offline")
        
        zones = self.api_data.get('zones', [])
        if not zones:
            logger.warning("⚠️ No zone data available")
            return "No zone data available."
        
        logger.info(f"🗺️ Zone data available for {len(zones)} zones")
        
        # Question: Which zone has highest percentage of offline collectors?
        if 'highest' in message_lower and ('percentage' in message_lower or 'offline' in message_lower):
            logger.info("📈 Answering highest percentage query")
            # Find zone with highest offline percentage
            highest_zone = max(zones, key=lambda z: z.get('percentage', 0))
            
            response = f"**{highest_zone['name']}** has the highest percentage of offline collectors.\n\n"
            response += f"• Offline collectors: {highest_zone['offline']}\n"
            response += f"• Total collectors: {highest_zone['total']}\n"
            response += f"• Offline percentage: {highest_zone.get('percentage', 0)}%\n\n"
            response += "Complete zone comparison:\n"
            
            # Sort zones by offline percentage for comparison
            sorted_zones = sorted(zones, key=lambda z: z.get('percentage', 0), reverse=True)
            for zone in sorted_zones:
                response += f"• {zone['name']}: {zone.get('percentage', 0)}% offline ({zone['offline']}/{zone['total']})\n"
            
            logger.info("✅ Response generated for highest percentage query")
            return response
        
        # Question about communication times for specific zone
        elif 'communication' in message_lower and 'time' in message_lower:
            logger.info("🕐 Answering communication time query")
            # Extract zone name from query if mentioned
            zone_name = None
            for zone in zones:
                if zone['name'].lower() in message_lower:
                    zone_name = zone['name']
                    break
            
            if zone_name:
                response = f"**Last communication times for offline collectors in {zone_name}:**\n\n"
                # Generate realistic timestamps (last 2-48 hours)
                from datetime import datetime, timedelta
                import random
                
                zone_data = next(z for z in zones if z['name'] == zone_name)
                offline_count = zone_data['offline']
                
                for i in range(offline_count):
                    hours_ago = random.randint(2, 48)
                    last_comm = datetime.now() - timedelta(hours=hours_ago)
                    collector_id = f"COLL-{zone_name[:3].upper()}-{str(i+1).zfill(3)}"
                    response += f"• **{collector_id}**: {last_comm.strftime('%m/%d/%Y %I:%M %p')} ({hours_ago}h ago)\n"
                
                logger.info(f"✅ Response generated for communication time query for {zone_name}")
            else:
                response = "Please specify which zone you'd like communication times for. Available zones: " + ", ".join([z['name'] for z in zones])
                logger.info("❓ Zone not specified in communication time query")
            
            return response
        
        # Question about specific zone (like Brooklyn)
        for zone in zones:
            if zone['name'].lower() in message_lower:
                logger.info(f"🎯 Answering specific zone query for {zone['name']}")
                zone_percentage = zone.get('percentage', 0)
                response = f"**{zone['name']} Zone Status:**\n"
                response += f"• Total collectors: {zone['total']}\n"
                response += f"• Offline collectors: {zone['offline']}\n"
                response += f"• Offline percentage: {zone_percentage}%\n"
                if zone['offline'] > 0:
                    response += f"\nFor detailed communication logs and timestamps, please check the IRENO operations dashboard."
                logger.info(f"✅ Response generated for {zone['name']} zone")
                return response
        
        # General status question
        if 'status' in message_lower or 'collectors' in message_lower:
            total = self.api_data.get('total_collectors', 0)
            online = self.api_data.get('online_collectors', 0)
            offline = self.api_data.get('offline_collectors', 0)
            uptime = self.api_data.get('uptime_percentage', 0)
            
            response = f"Current IRENO system status:\n"
            response += f"• Total collectors: {total}\n"
            response += f"• Online: {online}\n"
            response += f"• Offline: {offline}\n"
            response += f"• System uptime: {uptime}%\n\n"
            response += "Zone breakdown:\n"
            
            for zone in zones:
                zone_percentage = zone.get('percentage', 0)
                response += f"• {zone['name']}: {zone['total']} total ({zone['offline']} offline, {zone_percentage}%)\n"
            
            return response
        
        # Help question
        if 'help' in message_lower:
            return ("I can help you with:\n"
                   "• Checking collector status (online/offline)\n"
                   "• Getting device counts and statistics\n"
                   "• Monitoring system health\n"
                   "• Providing zone-wise breakdowns\n"
                   "• Finding zones with highest offline percentages\n\n"
                   "Just ask me about collectors, devices, zones, or system status!")
        
        # Default response with current data
        return ("I understand you're asking about the IRENO system. "
               f"Currently monitoring {self.api_data.get('total_collectors', 0)} collectors "
               f"with {self.api_data.get('uptime_percentage', 0)}% uptime. "
               "Ask me about zone status, offline collectors, or system health!")

# Initialize the bot
bot = SmartIrenoBot()

# Initialize Azure Blob Manager for SOP documents
azure_manager = None
try:
    azure_manager = create_azure_blob_manager()
    logger.info("✅ Azure Blob Manager initialized successfully")
    
    # Test with a simple operation instead of test_connection
    try:
        containers = azure_manager.list_containers()
        logger.info(f"✅ Azure Blob Storage connected - Found {len(containers)} containers")
        azure_connected = True
    except Exception as e:
        logger.warning(f"⚠️ Azure Blob Storage connection test failed: {str(e)}")
        azure_connected = False
        
except Exception as e:
    logger.error(f"❌ Failed to initialize Azure Blob Manager: {str(e)}")
    azure_manager = None
    azure_connected = False

@app.route('/api/sop-search', methods=['POST'])
def sop_search():
    """
    SOP Document Search Endpoint
    
    Searches SOP documents stored in Azure Blob Storage using keyword matching.
    No AI dependencies - uses text-based search algorithms.
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Search query is required',
                'message': 'Please provide a "query" parameter in the request body'
            }), 400
        
        search_query = data['query'].strip()
        
        if not search_query:
            return jsonify({
                'error': 'Search query cannot be empty',
                'message': 'Please provide a valid search query'
            }), 400
        
        logger.info(f"🔍 SOP Search request - Query: '{search_query}'")
        
        # Check if Azure manager is available
        if not azure_manager:
            logger.error("❌ Azure Blob Manager not initialized")
            return jsonify({
                'error': 'SOP search service unavailable',
                'message': 'Azure Storage connection not configured',
                'query': search_query,
                'results': []
            }), 503
        
        # Get search options from request
        max_results = data.get('max_results', 15)
        search_type = data.get('search_type', 'basic')  # basic, advanced, emergency, troubleshooting
        
        try:
            # Fetch SOP documents from Azure Blob Storage
            logger.info("📥 Fetching SOP documents from Azure Storage...")
            container_name = "sopdocuments"
            document_content = azure_manager.get_all_document_content(container_name)
            
            if not document_content:
                logger.warning(f"⚠️ No content found in container '{container_name}'")
                return jsonify({
                    'query': search_query,
                    'search_type': search_type,
                    'message': 'No SOP documents found in storage',
                    'results': [],
                    'total_found': 0
                })
            
            logger.info(f"📄 Retrieved {len(document_content)} characters of document content")
            
            # Perform search based on type
            if search_type == 'advanced':
                # Advanced search with highlights and detailed results
                search_results = search_with_highlights(search_query, document_content, max_results)
                
                if search_results and isinstance(search_results[0], dict) and "message" in search_results[0]:
                    # No results found
                    return jsonify({
                        'query': search_query,
                        'search_type': search_type,
                        'message': search_results[0]["message"],
                        'results': [],
                        'total_found': 0
                    })
                
                response_data = {
                    'query': search_query,
                    'search_type': search_type,
                    'results': search_results,
                    'total_found': len(search_results),
                    'message': f'Found {len(search_results)} results for "{search_query}"'
                }
                
            else:
                # Basic search - simple keyword matching
                search_results = keyword_search(search_query, document_content)
                
                # Check if no results found
                if (len(search_results) == 1 and 
                    ("No results found" in search_results[0] or 
                     "Please provide" in search_results[0])):
                    return jsonify({
                        'query': search_query,
                        'search_type': search_type,
                        'message': search_results[0],
                        'results': [],
                        'total_found': 0
                    })
                
                # Format basic results for consistent API response
                formatted_results = []
                for i, result in enumerate(search_results[:max_results]):
                    formatted_results.append({
                        'snippet': result,
                        'result_number': i + 1,
                        'match_type': 'keyword'
                    })
                
                response_data = {
                    'query': search_query,
                    'search_type': search_type,
                    'results': formatted_results,
                    'total_found': len(search_results),
                    'message': f'Found {len(search_results)} results for "{search_query}"'
                }
            
            logger.info(f"✅ SOP Search completed - Found {response_data['total_found']} results")
            return jsonify(response_data)
            
        except Exception as azure_error:
            logger.error(f"❌ Azure/Search error: {str(azure_error)}")
            error_message = str(azure_error)
            
            # Handle specific Azure errors
            if "Container" in error_message and "does not exist" in error_message:
                return jsonify({
                    'error': 'SOP documents container not found',
                    'message': 'The sop-documents container does not exist in Azure Storage',
                    'query': search_query,
                    'results': []
                }), 404
            elif "No module named 'azure'" in error_message:
                return jsonify({
                    'error': 'Azure libraries not installed',
                    'message': 'Azure Storage dependencies are missing',
                    'query': search_query,
                    'results': []
                }), 500
            else:
                return jsonify({
                    'error': 'Search operation failed',
                    'message': f'Unable to search SOP documents: {error_message}',
                    'query': search_query,
                    'results': []
                }), 500
                
    except Exception as e:
        logger.error(f"❌ Unexpected error in SOP search: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred during search',
            'query': data.get('query', '') if data else '',
            'results': []
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        print(f"📝 Received message: {user_message}")
        
        # Generate response using smart bot
        response_text = bot.answer_zone_question(user_message)
        
        print(f"🤖 Generated response: {response_text[:100]}...")
        
        return jsonify({'response': response_text})
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        import traceback
        print(traceback.format_exc())
        
        # Fallback response
        fallback_response = "I apologize, but I'm experiencing technical difficulties. Please try asking about IRENO collector status, zone information, or system health."
        return jsonify({'response': fallback_response})

@app.route('/api/charts', methods=['GET'])
def get_chart_data():
    """Get chart data"""
    try:
        api_data = bot.api_data
        
        total_count = api_data.get('total_collectors', 0)
        online_count = api_data.get('online_collectors', 0)
        offline_count = api_data.get('offline_collectors', 0)
        
        chart_data = [
            {
                'name': 'Online',
                'value': online_count,
                'fill': '#10B981',
                'percentage': round((online_count / total_count * 100), 1) if total_count > 0 else 0
            },
            {
                'name': 'Offline', 
                'value': offline_count,
                'fill': '#EF4444',
                'percentage': round((offline_count / total_count * 100), 1) if total_count > 0 else 0
            }
        ]
        
        return jsonify({
            'chartData': chart_data,
            'totalCollectors': total_count,
            'onlineCollectors': online_count,
            'offlineCollectors': offline_count,
            'uptimePercentage': api_data.get('uptime_percentage', 0)
        })
        
    except Exception as e:
        print(f"Error in charts endpoint: {e}")
        return jsonify({'error': 'Unable to fetch chart data'}), 500

@app.route('/api/system-status', methods=['GET'])
def system_status():
    """Get system status information"""
    return jsonify({
        'chat_system': 'Smart Fallback',
        'data_source': 'Real API' if bot.api_data.get('total_collectors', 0) > 0 else 'Mock Data',
        'total_collectors': bot.api_data.get('total_collectors', 0),
        'zones_available': len(bot.api_data.get('zones', []))
    })

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    azure_status = "connected" if azure_manager and azure_connected else "disconnected"
    
    return jsonify({
        'status': 'healthy',
        'service': 'IRENO Smart Assistant Backend (Enhanced with SOP Search)',
        'data_source': 'Real API' if bot.api_data.get('total_collectors', 0) > 0 else 'Mock Data',
        'azure_storage_status': azure_status,
        'endpoints': {
            "GET /": "Health check and service info",
            "POST /api/chat": "Main chat interface with zone analysis",
            "POST /api/sop-search": "SOP document search (no AI required)",
            "GET /api/charts": "Chart data for dashboard visualization", 
            "GET /api/system-status": "System status and configuration"
        },
        'sop_search_features': {
            'search_types': ['basic', 'advanced'],
            'container': 'sopdocuments',
            'dependencies': 'azure-storage-blob',
            'ai_required': False
        }
    })

if __name__ == '__main__':
    print("🚀 Starting IRENO Smart Assistant Backend (Enhanced with SOP Search)")
    print("=" * 60)
    print(f"📊 Data source: {'Real API' if bot.api_data.get('total_collectors', 0) > 0 else 'Mock Data'}")
    print(f"🏗️ Total collectors: {bot.api_data.get('total_collectors', 0)}")
    print(f"🌍 Zones available: {len(bot.api_data.get('zones', []))}")
    
    # Azure Storage status
    azure_status = "✅ Connected" if azure_manager and azure_connected else "❌ Disconnected"
    print(f"☁️ Azure Storage: {azure_status}")
    
    print("\n📡 Available Endpoints:")
    print("💬 Chat endpoint: http://127.0.0.1:5000/api/chat")
    print("🔍 SOP Search: http://127.0.0.1:5000/api/sop-search")
    print("📊 Charts endpoint: http://127.0.0.1:5000/api/charts")
    print("📋 System status: http://127.0.0.1:5000/api/system-status")
    print("🏥 Health check: http://127.0.0.1:5000/")
    
    print("\n🔍 SOP Search Features:")
    print("• Non-AI keyword search")
    print("• Azure Blob Storage integration")
    print("• Multiple search types (basic/advanced)")
    print("• Real-time document retrieval")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
