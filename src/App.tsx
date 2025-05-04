import React, { useContext, useState } from 'react';
import { DataProvider } from './contexts/DataContext';
import { ThemeContext } from './contexts/ThemeContext';
import { ChatProvider } from './contexts/ChatContext';
import { MetricsProvider } from './contexts/MetricsContext';
import TabNavigation from './components/TabNavigation';
import ChatView from './components/ChatView';
import DashboardView from './components/DashboardView';
import MetricsExplorerView from './components/MetricsExplorerView';
import ThemeToggle from './components/ThemeToggle';
import styles from './App.module.css';

// Define available tabs
const TABS = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'metrics', label: 'Explore Metrics' },
  { id: 'chat', label: 'Chat Assistant' },
];

// Removed AppContent as its logic is moved to DashboardView or will be in ChatView

// Removed AppProps interface as xLabelKey/yLabelKey are passed directly to DataProvider now

// Main App component sets up Providers and handles Tab Navigation
const App: React.FC = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const [activeTab, setActiveTab] = useState<string>(TABS[0].id); // Default to dashboard

  // Pass dummy keys for now, DataProvider might not need them anymore
  const dummyXLabelKey = "category"; 
  const dummyYLabelKey = "value";

  return (
    // DataProvider wraps everything so both views can potentially access context
    // Although DashboardView might fetch independently later as planned
    <DataProvider xLabelKey={dummyXLabelKey} yLabelKey={dummyYLabelKey}>
      <ChatProvider>
        <MetricsProvider>
    <div className={`${styles.appContainer} ${theme === 'dark' ? styles.darkTheme : ''}`}>
      <div className={styles.stickyHeader}>
        <header className={styles.header}>
          <h1 className={styles.mainTitle}>Enhanced Data App</h1>
          <div className={styles.themeToggleContainer}>
            <ThemeToggle />
          </div>
        </header>

        <TabNavigation
          tabs={TABS}
          activeTab={activeTab}
          onTabChange={setActiveTab}
        />
      </div>

      <main className={styles.scrollableContent}>
            {/* Conditionally render the active view */}
            {activeTab === 'dashboard' && <DashboardView />}
            {activeTab === 'metrics' && <MetricsExplorerView />}
            {activeTab === 'chat' && <ChatView />}
          </main>
        </div>
        </MetricsProvider>
      </ChatProvider>
    </DataProvider>
  );
};

export default App;
