# IRENO Backend API with RAG, Tool Calling, and SOP Search

Python Flask backend for the IRENO Smart Assistant with OpenAI, LangChain, real-time IRENO API integration, and non-AI SOP document search.

## Features
- 🤖 **OpenAI GPT-3.5-turbo** with function calling capabilities
- 🧠 **Conversation Memory** - Remembers last 10 messages
- 🔍 **RAG (Retrieval-Augmented Generation)** - Real-time data retrieval
- 🛠️ **Tool Calling** - Intelligent API selection based on user queries
- ⚡ **IRENO API Integration** - Live collector status and statistics
- 🎯 **Smart Agent** - Automatically chooses the right tool for each query
- 📄 **SOP Document Search** - Azure Blob Storage integration for Standard Operating Procedures
- 🔒 **Secure API key management** with environment variables
- 🌐 **CORS support** for React frontend integration
- 🚫 **No AI Dependencies for SOP Search** - Pure text-based keyword matching

## API Endpoints

### 1. Chat Endpoint
- **Route**: `POST /api/chat`
- **Purpose**: Main conversation interface with AI and tool calling

### 2. SOP Search Endpoint (NEW)
- **Route**: `POST /api/sop-search` 
- **Purpose**: Search Standard Operating Procedure documents
- **Request**: `{"query": "incident response", "search_type": "basic"}`
- **Response**: JSON with search results from Azure Blob Storage
- **Dependencies**: Azure Storage Blob, no AI required

### 3. Charts Data
- **Route**: `GET /api/charts`
- **Purpose**: Dashboard visualization data

## SOP Document Search (NEW)

The backend now includes Azure Blob Storage integration for searching Standard Operating Procedure documents without AI dependencies.

### Key Features
- 📄 **Azure Integration**: Connects to `irenointerns` storage account
- 🔍 **Keyword Search**: Text-based search with relevance scoring
- 🚫 **No AI Required**: Pure text processing, no external AI services
- 📁 **Multi-Document**: Searches across all .md files in `sopdocuments` container
- 🎯 **Context-Aware**: Provides file sources and surrounding text

### Usage Example
```bash
POST /api/sop-search
Content-Type: application/json

{
  "query": "incident response",
  "search_type": "basic",
  "max_results": 10
}
```

### Response Format
```json
{
  "query": "incident response",
  "results": [
    {
      "snippet": "[INCIDENT_RUNBOOK.md] # Incident Response Runbook...",
      "result_number": 1,
      "match_type": "keyword"
    }
  ],
  "total_found": 5,
  "message": "Found 5 results for 'incident response'"
}
```

## RAG Tools Available

### 1. Offline Collectors Tool
- **Endpoint**: `https://irenoakscluster.westus.cloudapp.azure.com/devicemgmt/v1/collector?status=offline`
- **Triggers**: "offline", "down", "disconnected", "not working", "failed"
- **Purpose**: Get information about collectors that are currently offline

### 2. Online Collectors Tool  
- **Endpoint**: `https://irenoakscluster.westus.cloudapp.azure.com/devicemgmt/v1/collector?status=online`
- **Triggers**: "online", "active", "connected", "working", "operational"
- **Purpose**: Get information about collectors that are currently online

### 3. Collectors Count Tool
- **Endpoint**: `https://irenoakscluster.westus.cloudapp.azure.com/devicemgmt/v1/collector/count`
- **Triggers**: "total", "count", "how many", "statistics", "overview"
- **Purpose**: Get total count and status summary of all collectors

## Example Queries and Tool Selection

| User Query | Tool Used | Response Type |
|------------|-----------|---------------|
| "How many collectors are offline?" | Offline Collectors | Count + List of offline devices |
| "Show me online devices" | Online Collectors | List of active collectors |
| "What's the total device count?" | Collectors Count | Total count + status breakdown |
| "Are there any failed collectors?" | Offline Collectors | Offline devices with details |
| "System overview please" | Collectors Count | Complete statistics summary |

## Setup Instructions

### 1. Install Python Dependencies

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The `.env` file is already created with your OpenAI API key. For production, make sure to:
- Keep the `.env` file secure and never commit it to version control
- Use proper environment variable management in production

### 3. Run the Flask Server

```bash
# Start the development server
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### POST /api/chat
Send a chat message to the RAG-enabled AI assistant with real-time IRENO data access.

**Request Body:**
```json
{
  "message": "How many collectors are offline?"
}
```

**Response:**
```json
{
  "response": "I found 3 offline collectors: Device-A at Site-1, Device-B at Site-2, and Device-C at Site-3. These devices need immediate attention to restore full system functionality."
}
```

### GET /health
Health check endpoint with feature information.

**Response:**
```json
{
  "status": "healthy",
  "service": "IRENO Backend API",
  "features": ["OpenAI Integration", "LangChain", "Conversation Memory", "RAG with Tool Calling", "IRENO API Integration"]
}
```

### GET /api/test-tools
Test endpoint to verify IRENO API tools connectivity and functionality.

**Response:**
```json
{
  "status": "success",
  "tools_test": {
    "offline_collectors": "Found 2 offline collectors...",
    "online_collectors": "Found 15 online collectors...",
    "collectors_count": "Total collectors: 17\n- Online: 15\n- Offline: 2..."
  },
  "timestamp": 1703097600
}
```

### POST /api/clear-memory
Clear the conversation memory (useful for starting fresh conversations).

**Response:**
```json
{
  "status": "success",
  "message": "Conversation memory cleared"
}
```

### GET /api/memory-status
Check the current state of conversation memory.

**Response:**
```json
{
  "message_count": 5,
  "memory_window": 10,
  "status": "active"
}
```

## AI Configuration

### Model Settings
- **Model**: GPT-3.5-turbo
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Memory Window**: 10 messages (last 5 exchanges)

### System Prompt
The AI is configured with a specialized system prompt for electric utility operations, focusing on:
- Real-time fault detection and resolution
- System status monitoring and reporting
- Performance analytics and efficiency optimization
- Maintenance scheduling and operational insights
- Grid load management and distribution
- Renewable energy source monitoring
- Regulatory compliance and reporting

## Development Notes
- Conversation memory persists during the Flask session
- Memory is cleared when the server restarts
- Verbose mode is enabled for debugging LangChain operations
- Error handling includes detailed error messages for development
