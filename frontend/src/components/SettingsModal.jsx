import React, { useState } from 'react';

const SettingsModal = ({ isOpen, onClose, onSaveApiKey, currentApiKey }) => {
  const [apiKey, setApiKey] = useState(currentApiKey || '');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (apiKey.trim()) {
      setIsLoading(true);
      try {
        await onSaveApiKey(apiKey.trim());
        onClose();
      } catch (error) {
        console.error('Failed to save API key:', error);
        alert('Failed to save API key. Please try again.');
      } finally {
        setIsLoading(false);
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="cyber-modal p-6 rounded-lg max-w-md w-full mx-4">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-cyber-green glow-text">
            API Configuration
          </h2>
          <button
            onClick={onClose}
            className="text-cyber-blue hover:text-cyber-purple transition-colors"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-cyber-blue mb-2">
              Gemini API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your Gemini API key..."
              className="w-full cyber-input p-3 rounded-lg"
              required
            />
            <p className="text-xs text-cyber-blue/60 mt-2">
              Your API key is stored locally in your browser session and never saved on our servers.
            </p>
          </div>

          <div className="mb-6">
            <div className="text-sm text-cyber-blue/80">
              <p className="mb-2">To get your Gemini API key:</p>
              <ol className="text-xs space-y-1 text-cyber-blue/60">
                <li>1. Visit <span className="text-cyber-green">ai.google.dev</span></li>
                <li>2. Sign in with your Google account</li>
                <li>3. Go to "Get API key" section</li>
                <li>4. Create a new API key</li>
                <li>5. Copy and paste it here</li>
              </ol>
            </div>
          </div>

          <div className="flex space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-cyber-gray hover:bg-cyber-light-gray border border-cyber-blue/30 text-cyber-blue py-3 rounded-lg transition-all duration-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!apiKey.trim() || isLoading}
              className="flex-1 cyber-button py-3 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin w-4 h-4 border-2 border-cyber-blue border-t-transparent rounded-full"></div>
                  <span>Saving...</span>
                </div>
              ) : (
                'Save Key'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SettingsModal;