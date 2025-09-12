import React, { useEffect, useRef } from 'react';
import Message from './Message';

const ChatWindow = ({ messages, isLoading }) => {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 cyber-grid">
      <div className="max-w-4xl mx-auto">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="cyber-card p-8 rounded-lg max-w-md mx-auto">
              <h2 className="text-xl font-bold text-cyber-green mb-4 glow-text">
                Welcome to Master Agentic AI
              </h2>
              <p className="text-cyber-blue/80 mb-4">
                A sophisticated Multi-Agent System implementing Constitutional AI principles.
              </p>
              <div className="text-sm text-cyber-blue/60">
                <p className="mb-2">Features:</p>
                <ul className="text-left space-y-1">
                  <li>• Planning Agent (Chain-of-Thought)</li>
                  <li>• Execution Agent (ReAct Framework)</li>
                  <li>• Ethics & Safety Review</li>
                  <li>• Tool Integration</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg, index) => (
            <Message
              key={index}
              message={msg.content}
              isUser={msg.role === 'user'}
              agentName={msg.agent}
              timestamp={msg.timestamp}
            />
          ))
        )}
        
        {isLoading && (
          <div className="mb-4 mr-8">
            <div className="cyber-card p-4 rounded-lg bg-cyber-dark/80 border-cyber-blue/30">
              <div className="flex items-center space-x-2">
                <div className="animate-pulse-slow w-2 h-2 bg-cyber-green rounded-full"></div>
                <div className="animate-pulse-slow w-2 h-2 bg-cyber-blue rounded-full" style={{animationDelay: '0.2s'}}></div>
                <div className="animate-pulse-slow w-2 h-2 bg-cyber-purple rounded-full" style={{animationDelay: '0.4s'}}></div>
                <span className="text-cyber-blue/80 text-sm ml-2">
                  Agents processing...
                </span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={chatEndRef} />
      </div>
    </div>
  );
};

export default ChatWindow;