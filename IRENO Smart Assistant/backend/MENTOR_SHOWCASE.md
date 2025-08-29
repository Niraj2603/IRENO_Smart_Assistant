# 🤖 IRENO Smart Assistant - Backend API (Mentor Showcase)

**AI-Powered Utility Management Assistant with RAG and Real-time API Integration**

## 🎯 Mentor Showcase Ready!

This is a production-ready Flask backend API that powers the IRENO Smart Assistant - an intelligent ChatGPT-style interface for electric utility management.

## ✨ Key Features

- **🧠 OpenAI GPT-3.5-turbo Integration** - Advanced conversational AI
- **🔧 LangChain RAG Framework** - Retrieval-Augmented Generation with tool calling
- **📡 Real-time IRENO API Integration** - Live data from utility systems
- **💾 Conversation Memory** - Context-aware multi-turn conversations
- **📊 Chart Data Generation** - Real-time visualization data
- **🛡️ Error Handling** - Robust fallbacks and error management
- **🌐 CORS Enabled** - Ready for React frontend integration

## 🚀 Quick Start for Mentor Demo

### 1. Start the Backend Server
```bash
python app.py
```

### 2. Run the Interactive Demo
```bash
# In a new terminal (keep the server running)
python showcase_demo.py
```

### 3. Test All Endpoints
```bash
python test_api.py
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check and service status |
| POST | `/api/chat` | Main chat interface with RAG capabilities |
| GET | `/api/charts` | Chart data for visualization |
| GET | `/api/test-tools` | Test IRENO API tools connectivity |
| POST | `/api/clear-memory` | Clear conversation memory |
| GET | `/api/memory-status` | Get current memory status |

## 🎬 Mentor Showcase Points

### Technical Excellence
- ✅ **No Deprecation Warnings** - Uses latest LangChain patterns
- ✅ **Modern Architecture** - OpenAI Functions with proper tool calling
- ✅ **Production Ready** - Comprehensive error handling and logging
- ✅ **Clean Code** - Well-documented and maintainable

### AI/ML Integration
- ✅ **Advanced RAG** - Real-time tool calling with IRENO APIs
- ✅ **Context Awareness** - Conversation memory and history
- ✅ **Smart Routing** - Intelligent tool selection based on user queries
- ✅ **Fallback Handling** - Graceful degradation when APIs are unavailable

### Real-world Application
- ✅ **Live Data Integration** - Connects to actual IRENO utility APIs
- ✅ **Domain Expertise** - Specialized knowledge for utility management
- ✅ **Practical Tools** - Offline/online collector monitoring, system stats
- ✅ **Visualization Ready** - Chart data generation for dashboards

## 🌟 Why This Impresses

1. **Production Quality** - Enterprise-ready code with proper architecture
2. **AI Innovation** - Cutting-edge RAG implementation with real-world application
3. **Technical Depth** - Complex integration of multiple AI/ML frameworks
4. **Practical Value** - Solves real utility management challenges
5. **Scalable Design** - Ready for deployment and feature expansion

---

**Ready to showcase the future of AI-powered utility management!** 🎉
