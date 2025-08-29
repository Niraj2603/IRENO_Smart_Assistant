import React, { useState, useRef } from 'react';
import { useApp } from '../context/AppContext';
import { Mic, Paperclip, Send } from 'lucide-react';
import styles from './ChatInput.module.css';

const ChatInput = () => {
  const { state, actions } = useApp();
  const [inputValue, setInputValue] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!inputValue.trim() || !state.activeConversation) return;

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    actions.addMessage(state.activeConversation.id, userMessage);
    setInputValue('');

    // Show typing indicator
    actions.setTyping(true);

    // Send message to backend API
    sendMessageToBackend(inputValue.trim());
  };

  const sendMessageToBackend = async (message) => {
    try {
      // Show typing indicator
      actions.setTyping(true);

      // Send request to Flask backend
      const response = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Create AI response message
      const aiResponse = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      // Add the response to the conversation
      actions.addMessage(state.activeConversation.id, aiResponse);
      
    } catch (error) {
      console.error('Error sending message to backend:', error);
      
      // Fallback response if backend is unavailable
      const errorResponse = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I'm having trouble connecting to the server right now. Please make sure the backend is running at http://127.0.0.1:5000. Error: ${error.message}`,
        timestamp: new Date()
      };
      
      actions.addMessage(state.activeConversation.id, errorResponse);
    } finally {
      // Hide typing indicator
      actions.setTyping(false);
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    
    // Auto-resize textarea
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleVoiceInput = () => {
    setIsRecording(!isRecording);
    // Voice input functionality would be implemented here
    console.log('Voice input toggled:', !isRecording);
  };

  const handleFileUpload = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log('File selected:', file.name);
      // File upload functionality would be implemented here
    }
  };

  const isInputEmpty = !inputValue.trim();

  return (
    <div className={styles.chatInputArea}>
      <form onSubmit={handleSubmit} className={styles.chatInputForm}>
        <div className={styles.inputContainer}>
          <button
            type="button"
            className={`${styles.voiceBtn} ${isRecording ? styles.recording : ''}`}
            onClick={handleVoiceInput}
            title="Voice Input"
            aria-label="Voice input"
          >
            <Mic size={16} />
          </button>
          
          <textarea
            ref={textareaRef}
            className={styles.chatInput}
            placeholder="Message IRENO Smart Assistant..."
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={state.isTyping}
          />
          
          <button
            type="button"
            className={styles.uploadBtn}
            onClick={handleFileUpload}
            title="Upload File"
            aria-label="Upload file"
          >
            <Paperclip size={16} />
          </button>
          
          <button
            type="submit"
            className={`${styles.sendBtn} ${isInputEmpty ? styles.disabled : ''}`}
            disabled={isInputEmpty || state.isTyping}
            title="Send message"
            aria-label="Send message"
          >
            <Send size={16} />
          </button>
        </div>
        
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx,.txt,.csv"
          style={{ display: 'none' }}
        />
      </form>
      
      <div className={styles.inputFooter}>
        <p>IRENO can make mistakes. Consider checking important information.</p>
      </div>
    </div>
  );
};

export default ChatInput;
