import React, { createContext, useState, ReactNode, useMemo } from 'react';

interface ChatMessage {
  id: string;
  question: string;
  answer: string;
  chartData: Record<string, unknown>[] | null;
  tableData: Record<string, unknown>[] | null;
  isMinimized: boolean;
  timestamp: Date;
}

interface ChatContextType {
  messages: ChatMessage[];
  addMessage: (question: string) => Promise<void>;
  toggleMinimize: (id: string) => void;
  isLoading: boolean;
}

const ChatContext = createContext<ChatContextType>({
  messages: [],
  addMessage: async () => {},
  toggleMinimize: () => {},
  isLoading: false,
});

export const ChatProvider: React.FC<{children: ReactNode}> = ({ children }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addMessage = async (question: string) => {
    setIsLoading(true);
    
    // Create temporary message
    const tempId = Date.now().toString();
    setMessages(prev => [
      ...prev.map(msg => ({...msg, isMinimized: true})), // Minimize all previous
      {
        id: tempId,
        question,
        answer: '',
        chartData: null,
        tableData: null,
        isMinimized: false,
        timestamp: new Date()
      }
    ]);

    try {
      const response = await fetch('http://localhost:5001/api/data');
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      setMessages(prev => prev.map(msg => 
        msg.id === tempId ? {
          ...msg,
          answer: "Here's the analysis of your data",
          chartData: data,
          tableData: data
        } : msg
      ));
    } catch (error) {
      setMessages(prev => prev.map(msg => 
        msg.id === tempId ? {
          ...msg,
          answer: error instanceof Error ? error.message : 'Failed to load data',
          chartData: null,
          tableData: null
        } : msg
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMinimize = (id: string) => {
    setMessages(prev => prev.map(msg => 
      msg.id === id ? {...msg, isMinimized: !msg.isMinimized} : msg
    ));
  };

  const value = useMemo(() => ({
    messages,
    addMessage,
    toggleMinimize,
    isLoading
  }), [messages, isLoading]);

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export default ChatContext;
