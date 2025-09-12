import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import SettingsModal from './components/SettingsModal';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [apiKey, setApiKey] = useState('');

  // Load API key from session storage on component mount
  useEffect(() => {
    const savedApiKey = sessionStorage.getItem('gemini_api_key');
    if (savedApiKey) {
      setApiKey(savedApiKey);
      // Set the API key on the backend
      setApiKeyOnBackend(savedApiKey);
    } else {
      // Show settings modal if no API key is saved
      setIsSettingsOpen(true);
    }
  }, []);

  const setApiKeyOnBackend = async (key) => {
    try {
      await axios.post(`${API_BASE_URL}/set-api-key`, {
        api_key: key
      });
    } catch (error) {
      console.error('Failed to set API key on backend:', error);
      throw error;
    }
  };

  const handleSaveApiKey = async (newApiKey) => {
    try {
      await setApiKeyOnBackend(newApiKey);
      sessionStorage.setItem('gemini_api_key', newApiKey);
      setApiKey(newApiKey);
    } catch (error) {
      throw error;
    }
  };

  const addMessage = (content, role = 'user', agent = null) => {
    const newMessage = {
      content,
      role,
      agent,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, newMessage]);
    return newMessage;
  };

  const handleSendMessage = async (messageContent) => {
    if (!apiKey) {
      setIsSettingsOpen(true);
      return;
    }

    // Add user message
    addMessage(messageContent, 'user');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageContent,
          conversation_history: messages.slice(-10) // Send last 10 messages for context
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim());

        for (const line of lines) {
          try {
            const data = JSON.parse(line);
            
            if (data.type === 'status') {
              // Update the last message or add a new status message
              setMessages(prev => {
                const lastMessage = prev[prev.length - 1];
                if (lastMessage && lastMessage.role === 'status') {
                  // Update the last status message
                  return [
                    ...prev.slice(0, -1),
                    {
                      content: `${data.agent}: ${data.message}`,
                      role: 'status',
                      agent: data.agent,
                      timestamp: new Date().toISOString()
                    }
                  ];
                } else {
                  // Add new status message
                  return [
                    ...prev,
                    {
                      content: `${data.agent}: ${data.message}`,
                      role: 'status',
                      agent: data.agent,
                      timestamp: new Date().toISOString()
                    }
                  ];
                }
              });
            } else if (data.type === 'response') {
              // Remove any status messages and add the final response
              setMessages(prev => {
                const messagesWithoutStatus = prev.filter(msg => msg.role !== 'status');
                return [
                  ...messagesWithoutStatus,
                  {
                    content: data.message,
                    role: 'assistant',
                    agent: data.agent,
                    timestamp: new Date().toISOString()
                  }
                ];
              });
            } else if (data.type === 'error') {
              // Remove any status messages and add error message
              setMessages(prev => {
                const messagesWithoutStatus = prev.filter(msg => msg.role !== 'status');
                return [
                  ...messagesWithoutStatus,
                  {
                    content: `Error: ${data.message}`,
                    role: 'assistant',
                    agent: 'System',
                    timestamp: new Date().toISOString()
                  }
                ];
              });
            }
          } catch (parseError) {
            console.error('Failed to parse response chunk:', parseError);
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      addMessage(
        `Sorry, I encountered an error: ${error.message}. Please check your API key and try again.`,
        'assistant',
        'System'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cyber-dark flex flex-col">
      {/* Header */}
      <header className="border-b border-cyber-blue/30 bg-cyber-darker/90 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-cyber-green glow-text">
              Master Agentic AI
            </h1>
            <p className="text-sm text-cyber-blue/70">
              Multi-Agent System • Constitutional AI • ReAct Framework
            </p>
          </div>
          <button
            onClick={() => setIsSettingsOpen(true)}
            className="cyber-button p-3 rounded-lg"
            title="Settings"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
        </div>
      </header>

      {/* Chat Area */}
      <ChatWindow messages={messages} isLoading={isLoading} />

      {/* Input Area */}
      <InputBar onSendMessage={handleSendMessage} disabled={isLoading || !apiKey} />

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSaveApiKey={handleSaveApiKey}
        currentApiKey={apiKey}
      />
    </div>
  );
}

export default App;