import React from 'react';

const Message = ({ message, isUser, agentName, timestamp }) => {
  return (
    <div className={`mb-4 ${isUser ? 'ml-8' : 'mr-8'}`}>
      <div className={`cyber-card p-4 rounded-lg ${
        isUser ? 'bg-cyber-purple/20 border-cyber-purple/30' : 'bg-cyber-dark/80 border-cyber-blue/30'
      }`}>
        <div className="flex items-center justify-between mb-2">
          <span className={`text-sm font-semibold ${
            isUser ? 'text-cyber-purple' : 'text-cyber-green'
          }`}>
            {isUser ? 'You' : agentName || 'Master Agentic AI'}
          </span>
          {timestamp && (
            <span className="text-xs text-cyber-blue/60">
              {new Date(timestamp).toLocaleTimeString()}
            </span>
          )}
        </div>
        <div className={`text-sm leading-relaxed ${
          isUser ? 'text-cyber-purple/90' : 'text-cyber-blue/90'
        }`}>
          {message}
        </div>
      </div>
    </div>
  );
};

export default Message;