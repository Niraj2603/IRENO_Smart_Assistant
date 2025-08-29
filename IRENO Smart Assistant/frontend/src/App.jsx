import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
import LoginPage from './pages/LoginPage';
import MainApp from './pages/MainApp';

function AppContent() {
  const { state, actions } = useApp();

  const handleLogin = (user) => {
    actions.setUser(user);
  };

  if (!state.currentUser) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return <MainApp />;
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
