import React, { useContext, useRef, useEffect, useState } from 'react';
import ChatContext from '../contexts/ChatContext';
import { ThemeContext } from '../contexts/ThemeContext';
import GenericGraph from './GenericGraph';
import DataTable from './DataTable';
import styles from './ChatView.module.css';

const ChatView: React.FC = () => {
  const { messages, addMessage, toggleMinimize, isLoading } = useContext(ChatContext);
  const { theme } = useContext(ThemeContext);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      addMessage(inputValue);
      setInputValue('');
    }
  };

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`${styles.message} ${message.isMinimized ? styles.minimized : ''}`}
          >
            <div className={styles.question}>
              <strong>You:</strong> {message.question}
              <button 
                onClick={() => toggleMinimize(message.id)}
                className={styles.minimizeButton}
              >
                {message.isMinimized ? '+' : '-'}
              </button>
            </div>
            
            {!message.isMinimized && (
              <div className={styles.answer}>
                <div className={styles.answerText}>
                  <strong>Assistant:</strong> {message.answer}
                </div>
                {message.chartData && (
                  <div className={styles.chartContainer}>
                    <GenericGraph 
                      initialChartType="bar"
                      title={`Analysis: ${message.question}`}
                      data={message.chartData}
                    />
                  </div>
                )}
                {message.tableData && (
                  <div className={styles.tableContainer}>
                    <DataTable 
                      data={message.tableData as Record<string, string | number | boolean | null>[]} 
                    />
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        {isLoading && <div className={styles.loading}>Loading response...</div>}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className={styles.inputForm}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about your data..."
          className={styles.inputField}
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className={styles.submitButton}
          disabled={isLoading}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatView;
