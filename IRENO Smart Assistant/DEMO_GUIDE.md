# IRENO Smart Assistant Demo Guide

## Quick Start

### Option 1: Automated Launch (Recommended)
Simply double-click the `start_demo.bat` file to start both frontend and backend servers automatically.

### Option 2: Manual Launch

#### Backend (Flask Server)
```bash
cd backend
python app_working.py
```

#### Frontend (React + Vite)
```bash
cd frontend
npm run dev
```

## Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## Features Available

### 1. SOP Document Search
- Navigate to the chat interface
- Type queries related to SOP documents
- The system will search through Azure Blob Storage documents
- Get relevant document excerpts and information

### 2. Chat Interface
- Modern ChatGPT-style interface
- Real-time responses
- Conversation history
- Dark/Light theme toggle

### 3. Authentication
- Login page with role-based access
- Support for different user types (Field Technician, Command Center, Leadership)

## Demo Flow

1. **Start the application** using `start_demo.bat`
2. **Open browser** to http://localhost:5173
3. **Login** with desired role
4. **Try SOP searches** like:
   - "incident response procedures"
   - "safety protocols"
   - "emergency shutdown"
   - "maintenance guidelines"

## Troubleshooting

### Frontend Issues
- Ensure Node.js is installed
- Run `npm install` in the frontend directory
- Check if port 5173 is available

### Backend Issues
- Ensure Python 3.x is installed
- Install dependencies: `pip install -r backend/requirements.txt`
- Check if port 5000 is available
- Verify Azure connection string in .env file

### Environment Variables
Create a `.env` file in the backend directory with:
```
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
```
