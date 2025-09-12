import React, { useState } from 'react';

const InputBar = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="border-t border-cyber-blue/30 bg-cyber-darker/90 backdrop-blur-sm">
      <div className="max-w-4xl mx-auto p-4">
        <form onSubmit={handleSubmit} className="flex space-x-4">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your message to the Master Agentic AI..."
            disabled={disabled}
            className="flex-1 cyber-input p-3 rounded-lg resize-none min-h-[50px] max-h-[120px]"
            rows="2"
          />
          <button
            type="submit"
            disabled={disabled || !message.trim()}
            className="cyber-button px-6 py-3 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {disabled ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin w-4 h-4 border-2 border-cyber-blue border-t-transparent rounded-full"></div>
                <span>Processing</span>
              </div>
            ) : (
              'Send'
            )}
          </button>
        </form>
        
        <div className="mt-2 text-xs text-cyber-blue/50 text-center">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default InputBar;