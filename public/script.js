async function processText() {
    const useCase = document.getElementById('useCase').value;
    const loadingIndicator = document.getElementById('loadingIndicator');
    const summaryOutput = document.getElementById('summaryOutput');
    
    try {
        // Show loading indicator
        loadingIndicator.style.display = 'flex';
        summaryOutput.innerHTML = '';

        // Get file or text
        const fileInput = document.getElementById('fileInput');
        const textInput = document.getElementById('textInput');

        let response;
        if (fileInput.files.length > 0) {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('useCase', useCase);

            response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
        } else if (textInput.value.trim()) {
            response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: textInput.value,
                    useCase: useCase
                })
            });
        } else {
            throw new Error('Please enter text or upload a file');
        }

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        // Display the summary
        summaryOutput.innerHTML = data.text;
    } catch (error) {
        summaryOutput.innerHTML = `Error: ${error.message}`;
    } finally {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
    }
} 