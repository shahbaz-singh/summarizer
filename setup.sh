# Install Node.js dependencies
npm install express cors multer tesseract.js pdf-parse dotenv

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install python-dotenv phi-client openai

# Start the server
npm start 