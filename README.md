# AI Document & Text Summarizer

An AI-powered application that summarizes both text and documents using GPT-4 Vision, with support for different use cases like legal, technical, and medical documents.

## Features
- 📝 Text summarization
- 📄 Document/Image summarization
- ⚖️ Specialized summaries (Legal, Medical, Technical, Academic)
- 🔄 Real-time processing
- 📊 Structured output format

## Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd <project-directory>
```

2. **Create and set up Python virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. **Install Python dependencies**
```bash
pip install python-dotenv phi-client openai
```

4. **Install Node.js dependencies**
```bash
npm install
```

5. **Create environment file**
Create a `.env` file in the root directory with your OpenAI API key:
```plaintext
OPENAI_API_KEY=your_api_key_here
PORT=3000
```

## Running the Application

1. **Start the server**
```bash
npm start
```

2. **Access the application**
Open your browser and navigate to:
```
http://localhost:3000
```

## Usage

1. **Text Summarization**
   - Enter or paste your text in the input box
   - Select the appropriate use case (General, Legal, Technical, etc.)
   - Click "Summarize"

2. **Document Summarization**
   - Click "Upload PDF or Image"
   - Select your document
   - Choose the use case
   - Click "Summarize"

## Supported File Types
- Images (PNG, JPEG, GIF, WebP)
- Text files
- PDFs (coming soon)

## Troubleshooting

1. **API Key Error**
   - Ensure your OpenAI API key is correctly set in the `.env` file
   - Make sure there are no spaces or quotes around the API key

2. **Python Environment Issues**
   - Make sure the virtual environment is activated
   - Verify all Python dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

3. **Node.js Issues**
   - Clear node_modules and reinstall dependencies
   ```bash
   rm -rf node_modules
   npm install
   ```

## Project Structure
```
.
├── server.js              # Express server
├── summarization.py       # Python summarization script
├── public/
│   ├── index.html        # Frontend interface
│   └── styles.css        # Styles
├── .env                  # Environment variables
└── package.json          # Node.js dependencies
```

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Server port (default: 3000)

## Dependencies
### Python
- python-dotenv
- phi-client
- openai

### Node.js
- express
- cors
- multer
- dotenv

## License
MIT

## Support
For issues and feature requests, please open an issue on the repository. 