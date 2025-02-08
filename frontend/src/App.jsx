import { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState({ type: 'idle', message: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) {
      setStatus({ type: 'error', message: 'Please enter some text to summarize' });
      return;
    }

    setIsLoading(true);
    setStatus({ type: 'loading', message: 'Generating summary...' });

    try {
      const response = await fetch('http://localhost:3001/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await response.json();
      setSummary(data.summary);
      setStatus({ type: 'success', message: 'Summary generated successfully!' });
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to generate summary' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>✨ AI Text Summarizer</h1>
        <p className="subtitle">Transform long text into concise summaries</p>
      </header>

      <main>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="input-text">Enter your text:</label>
            <textarea
              id="input-text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste your text here..."
              disabled={isLoading}
            />
          </div>

          <button 
            type="submit" 
            className={`submit-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Summarizing...' : '✨ Summarize'}
          </button>

          {status.message && (
            <div className={`status-message ${status.type}`}>
              {status.message}
            </div>
          )}

          {summary && (
            <div className="output-group">
              <label>Summary:</label>
              <div className="summary-content">
                {summary}
              </div>
            </div>
          )}
        </form>
      </main>
    </div>
  );
}

export default App; 