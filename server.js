const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const multer = require('multer');
const Tesseract = require('tesseract.js');
const fs = require('fs');
const pdfParse = require('pdf-parse');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files from public directory
app.use(express.static('public'));

const upload = multer({ dest: 'uploads/' });

app.post('/summarize', async (req, res) => {
  try {
    const { text, useCase } = req.body;

    if (!text) {
      return res.status(400).json({ error: 'No text provided' });
    }

    console.log('Processing text with useCase:', useCase);

    const pythonProcess = spawn('python', ['summarization.py']);
    let summary = '';
    let error = '';

    // Send metadata and text together
    const input = JSON.stringify({
      text: text,
      useCase: useCase,
      isText: true
    }) + '\n';

    pythonProcess.stdin.write(input);
    pythonProcess.stdin.end();

    pythonProcess.stdout.on('data', (data) => {
      summary += data.toString();
      console.log('Python stdout:', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      error += data.toString();
      console.error('Python stderr:', data.toString());
    });

    await new Promise((resolve, reject) => {
      pythonProcess.on('close', (code) => {
        console.log('Python process exited with code:', code);
        if (code !== 0) {
          reject(new Error(`Python process exited with code ${code}\n${error}`));
        } else {
          resolve();
        }
      });
    });

    res.json({ summary: summary.trim() });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to generate summary' });
  }
});

app.post('/upload', upload.single('file'), async (req, res) => {
    try {
        const file = req.file;
        const useCase = req.body.useCase || 'general';

        if (!file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        const supportedFormats = ['image/png', 'image/jpeg', 'image/gif', 'image/webp'];
        if (!supportedFormats.includes(file.mimetype)) {
            return res.status(400).json({ 
                error: 'Unsupported file format. Please upload a PNG, JPEG, GIF, or WebP image.'
            });
        }

        const fileBuffer = fs.readFileSync(file.path);
        console.log('File buffer size:', fileBuffer.length);

        // Create Python process with error handling
        const pythonProcess = spawn('python', ['summarization.py']);
        let summary = '';
        let error = '';

        // Handle process errors
        pythonProcess.on('error', (err) => {
            console.error('Failed to start Python process:', err);
        });

        // Handle stdin errors without crashing
        pythonProcess.stdin.on('error', (err) => {
            if (err.code === 'EPIPE') {
                console.log('Python process closed stdin');
            } else {
                console.error('Error writing to Python stdin:', err);
            }
        });

        // Set up data handlers before writing
        pythonProcess.stdout.on('data', (data) => {
            summary += data.toString();
            console.log('Python stdout:', data.toString());
        });

        pythonProcess.stderr.on('data', (data) => {
            error += data.toString();
            console.error('Python stderr:', data.toString());
        });

        // Write data with proper error handling
        try {
            // Send metadata
            const metadata = JSON.stringify({ useCase, fileSize: fileBuffer.length }) + '\n';
            await new Promise((resolve, reject) => {
                pythonProcess.stdin.write(metadata, (err) => {
                    if (err) reject(err);
                    else resolve();
                });
            });

            // Send file data
            await new Promise((resolve, reject) => {
                pythonProcess.stdin.write(fileBuffer, (err) => {
                    if (err) reject(err);
                    else resolve();
                });
            });

            // End the stream
            pythonProcess.stdin.end();
        } catch (err) {
            console.error('Error writing to Python process:', err);
        }

        // Clean up the temp file
        fs.unlinkSync(file.path);

        // Wait for process to complete
        await new Promise((resolve, reject) => {
            pythonProcess.on('close', (code) => {
                console.log('Python process exited with code:', code);
                if (code !== 0) {
                    reject(new Error(`Python process exited with code ${code}\n${error}`));
                } else {
                    resolve();
                }
            });
        });

        if (summary) {
            res.json({ text: summary.trim() });
        } else {
            throw new Error('No summary generated');
        }
    } catch (error) {
        console.error('Upload error:', error);
        res.status(500).json({ error: 'Failed to process file: ' + error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 