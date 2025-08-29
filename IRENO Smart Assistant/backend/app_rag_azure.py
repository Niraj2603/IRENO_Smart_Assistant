from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from ireno_tools import create_ireno_tools

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('ireno_assistant.log', mode='a', encoding='utf-8')  # File output
    ]
)

# Set specific log levels for different components
logging.getLogger('werkzeug').setLevel(logging.INFO)  # Flask server logs
logging.getLogger('httpx').setLevel(logging.INFO)     # HTTP request logs
logging.getLogger('langchain').setLevel(logging.INFO) # LangChain logs
logging.getLogger('requests').setLevel(logging.INFO)  # API request logs

logger = logging.getLogger(__name__)

# Log startup information
logger.info("=" * 80)
logger.info("🚀 IRENO Smart Assistant - Backend Starting Up")
logger.info("=" * 80)

# Global variables for agent components
agent_executor = None
memory = None

def initialize_azure_openai():
    """Initialize Azure OpenAI with the exact configuration from the demo notebook"""
    try:
        # Get API key from environment
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        if not api_key:
            raise ValueError("AZURE_OPENAI_API_KEY not found in environment variables")
        
        # Create Azure OpenAI instance with exact notebook configuration
        azure_llm = AzureChatOpenAI(
            azure_deployment="gpt-4o",
            openai_api_version="2025-01-01-preview",
            azure_endpoint="https://ireno-interns-openai.openai.azure.com/",
            api_key=api_key,
            temperature=0
        )
        
        logger.info("✅ Azure OpenAI initialized successfully")
        return azure_llm
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Azure OpenAI: {str(e)}")
        raise

def create_chat_prompt():
    """Create an enhanced ChatPromptTemplate with comprehensive KPI management capabilities"""
    system_prompt = """You are the IRENO Smart Assistant - an expert AI assistant for electric utility management and smart grid operations.

🎯 MISSION: Provide real-time insights, performance analytics, and operational support for electric utility systems.

📊 AVAILABLE CAPABILITIES:

**COLLECTOR MANAGEMENT:**
- get_offline_collectors: Monitor offline/disconnected devices
- get_online_collectors: Track active/operational devices  
- get_collectors_count: Get comprehensive collector statistics

**KPI & PERFORMANCE ANALYTICS:**
- get_daily_interval_read_success_percentage: Today's interval read performance
- get_daily_register_read_success_percentage: Today's register read performance
- get_last_7_days_interval_read_success: Weekly interval read trends
- get_last_7_days_register_read_success: Weekly register read trends

**ZONE-BASED ANALYTICS:**
- get_interval_read_success_by_zone_daily/weekly/monthly: Zone performance comparison
- get_register_read_success_by_zone_daily/weekly/monthly: Zone register performance
- get_comprehensive_kpi_summary: Executive dashboard with all key metrics

**RESPONSE GUIDELINES:**
✅ Always use real-time tools to get current data before responding
✅ Provide actionable insights with specific metrics and percentages
✅ Highlight performance issues and improvement opportunities
✅ Use clear formatting with headers, bullet points, and emojis for readability
✅ Suggest follow-up actions when performance is below optimal
✅ Compare current performance with historical trends when available

**EXPERTISE AREAS:**
- Smart grid operations and monitoring
- Utility performance optimization
- Real-time system diagnostics
- Trend analysis and forecasting
- Zone-based performance comparison
- KPI dashboard creation and analysis

**TONE:** Professional, technical, actionable - suitable for utility operators, field technicians, and management.

Remember: You have access to comprehensive real-time utility data - always leverage these tools to provide accurate, up-to-date insights and recommendations."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    return prompt

def initialize_agent():
    """Initialize the RAG and Tool Calling agent"""
    global agent_executor, memory
    
    try:
        # Initialize Azure OpenAI
        azure_llm = initialize_azure_openai()
        
        # Get live tools from ireno_tools.py
        tools = create_ireno_tools()
        logger.info(f"✅ Created {len(tools)} live API tools")
        
        # Create conversation memory with k=10 as specified
        memory = ConversationBufferWindowMemory(
            k=10,
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create chat prompt template
        prompt = create_chat_prompt()
        
        # Create tool calling agent
        agent = create_tool_calling_agent(
            llm=azure_llm,
            tools=tools,
            prompt=prompt
        )
        
        # Create agent executor with memory and verbose logging
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
        
        logger.info("✅ RAG and Tool Calling agent initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check if agent is initialized
        agent_status = "initialized" if agent_executor is not None else "not initialized"
        
        # Check environment variables
        azure_key_status = "configured" if os.getenv('AZURE_OPENAI_API_KEY') else "missing"
        
        return jsonify({
            "status": "healthy",
            "agent": agent_status,
            "azure_openai_key": azure_key_status,
            "tools": "live API integration",
            "memory": "conversation buffer (k=10)",
            "model": "gpt-4o via Azure OpenAI"
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint that processes user messages through the RAG agent"""
    try:
        # Check if agent is initialized
        if agent_executor is None:
            return jsonify({
                "error": "Agent not initialized. Please check server logs."
            }), 500
        
        # Get user message from request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' field in request body"
            }), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        logger.info(f"🤖 Processing user message: {user_message}")
        
        # Invoke the agent executor with the user's message
        try:
            logger.info("🔄 Invoking agent executor...")
            response = agent_executor.invoke({
                "input": user_message
            })
            logger.info(f"✅ Agent executor completed successfully")
            
        except Exception as agent_error:
            logger.error("=" * 80)
            logger.error("❌ AGENT EXECUTION ERROR DETAILS:")
            logger.error("=" * 80)
            logger.error(f"❌ Error message: {str(agent_error)}")
            logger.error(f"❌ Error type: {type(agent_error).__name__}")
            logger.error(f"❌ User message that caused error: {user_message}")
            logger.error("❌ Full stack trace:")
            logger.error("", exc_info=True)
            logger.error("=" * 80)
            
            # Return a user-friendly error response
            return jsonify({
                "error": "I encountered an issue processing your request. Please try again or rephrase your question.",
                "details": f"Error type: {type(agent_error).__name__}",
                "status": "error"
            }), 500
        
        # Extract the agent's response
        agent_response = response.get('output', 'Sorry, I could not generate a response.')
        
        logger.info(f"✅ Agent response generated successfully")
        
        return jsonify({
            "response": agent_response,
            "status": "success"
        }), 200
        
    except Exception as e:
        # Enhanced error logging for debugging
        logger.error("=" * 80)
        logger.error("❌ CHAT ENDPOINT ERROR DETAILS:")
        logger.error("=" * 80)
        logger.error(f"❌ Error message: {str(e)}")
        logger.error(f"❌ Exception type: {type(e).__name__}")
        logger.error(f"❌ Request data: {request.get_json() if request.is_json else 'No JSON data'}")
        logger.error(f"❌ Request method: {request.method}")
        logger.error(f"❌ Request URL: {request.url}")
        logger.error("❌ Full traceback:")
        logger.error("", exc_info=True)
        
        # Check for specific error types
        if "openai" in str(type(e)).lower() or "azure" in str(type(e)).lower():
            logger.error("🔍 AZURE OPENAI API ERROR DETECTED:")
            logger.error("   - Check if API key is valid and not expired")
            logger.error("   - Verify network connectivity to Azure OpenAI")
            logger.error("   - Ensure Azure OpenAI service is running")
            logger.error("   - Check if deployment name 'gpt-4o' exists")
        elif "connection" in str(e).lower():
            logger.error("🔍 CONNECTION ERROR DETECTED:")
            logger.error("   - Check network connectivity")
            logger.error("   - Verify IRENO API endpoints are accessible")
            logger.error("   - Check firewall settings")
        elif "timeout" in str(e).lower():
            logger.error("🔍 TIMEOUT ERROR DETECTED:")
            logger.error("   - API response taking too long")
            logger.error("   - Consider increasing timeout values")
            logger.error("   - Check API server load")
        
        logger.error("=" * 80)
        
        return jsonify({
            "error": f"Connection error.",
            "details": str(e),
            "status": "error"
        }), 500

@app.route('/api/reset-memory', methods=['POST'])
def reset_memory():
    """Reset the conversation memory"""
    try:
        global memory
        if memory:
            memory.clear()
            logger.info("✅ Conversation memory reset")
            return jsonify({"status": "success", "message": "Memory reset successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Memory not initialized"}), 500
    except Exception as e:
        logger.error(f"❌ Memory reset error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting IRENO Smart Grid RAG Assistant with Azure OpenAI...")
    print("=" * 60)
    
    # Initialize the agent
    if initialize_agent():
        print("✅ Agent initialization successful!")
        print(f"🔧 Tools: Live API integration via ireno_tools.py")
        print(f"🧠 Model: GPT-4o via Azure OpenAI")
        print(f"💾 Memory: Conversation Buffer (k=10)")
        print(f"🌐 Endpoint: POST /api/chat")
        print("=" * 60)
        
        # Start Flask development server
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Agent initialization failed! Check logs for details.")
        print("💡 Make sure AZURE_OPENAI_API_KEY is set in your .env file")
