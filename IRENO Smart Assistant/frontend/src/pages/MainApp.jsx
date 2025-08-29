import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import AppHeader from '../components/AppHeader';
import ConversationSidebar from '../components/ConversationSidebar';
import MainChat from '../components/MainChat';
import SettingsModal from '../components/SettingsModal';
import styles from './MainApp.module.css';

const MainApp = () => {
  const { state } = useApp();
  const [settingsOpen, setSettingsOpen] = useState(false);

  const handleOpenSettings = () => setSettingsOpen(true);
  const handleCloseSettings = () => setSettingsOpen(false);

  return (
    <div className={styles.appContainer}>
      <AppHeader onOpenSettings={handleOpenSettings} />
      <div className={styles.appBody}>
        <ConversationSidebar />
        <MainChat />
      </div>
      <SettingsModal 
        isOpen={settingsOpen} 
        onClose={handleCloseSettings} 
      />
    </div>
  );
};

export default MainApp;
