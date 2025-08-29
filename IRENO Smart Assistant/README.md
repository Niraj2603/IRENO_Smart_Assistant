# IRENO Smart Assistant

A React-based ChatGPT-style AI interface for electric utilities with Python Flask backend.

## Project Structure

```
ireno-react-app-Frontend/
├── frontend/             # React frontend application
│   ├── src/             # React source code
│   ├── public/          # Static assets
│   ├── package.json     # Frontend dependencies
│   └── vite.config.js   # Vite configuration
├── backend/             # Python Flask backend
│   ├── app_working.py   # Main Flask application
│   ├── azure_blob_handler.py  # Azure Storage integration
│   ├── sop_search.py    # SOP document search
│   └── requirements.txt # Backend dependencies
└── docs/                # Documentation
```

## Frontend Setup (React + Vite)

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Backend Setup (Python Flask)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Flask Server
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## Features

### Frontend
- 🔐 **Login Page** - Role-based authentication (Field Technician, Command Center, Senior Leadership)
- 💬 **Chat Interface** - Real-time messaging with AI assistant
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🌓 **Theme Toggle** - Light and dark mode support
- 📂 **Conversation Management** - Create, organize, and delete conversations
- ⚡ **Quick Prompts** - Pre-built prompts for common utility tasks
- 🎙️ **Voice Input** - Voice recording capability (UI ready)
- 📎 **File Upload** - Document upload support (UI ready)

### Backend
- 🚀 **REST API** - Flask-based API with CORS support
- 💬 **Chat Endpoint** - `/api/chat` for message processing
- 🏥 **Health Check** - `/health` endpoint for monitoring
- 🔄 **Echo Response** - Currently echoes user input (ready for AI integration)

## Development

### Running Both Services
1. **Terminal 1 - Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   npm run dev
   ```

### API Integration
The frontend automatically connects to the Flask backend at `http://127.0.0.1:5000/api/chat`. If the backend is unavailable, error messages will be displayed in the chat.

## Technologies Used

### Frontend
- React 18
- Vite (build tool)
- Lucide React (icons)
- CSS Modules (styling)

### Backend
- Python 3.8+
- Flask 3.0.0
- Flask-CORS 4.0.0

## Next Steps
- Replace echo response with actual AI/LLM integration
- Add user authentication and session management
- Implement conversation persistence
- Add file processing capabilities
- Integrate voice recognition and synthesis+ Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
