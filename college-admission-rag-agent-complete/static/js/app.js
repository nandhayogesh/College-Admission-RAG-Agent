// College Admission RAG Agent - Frontend JavaScript

class CollegeAdmissionAgent {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.fileInput = document.getElementById('fileInput');
        this.uploadButton = document.getElementById('uploadButton');

        this.initializeEventListeners();
        this.checkSystemStatus();

        // Auto-focus on input
        this.messageInput.focus();
    }

    initializeEventListeners() {
        // Send message on Enter key or button click
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Quick questions
        document.querySelectorAll('.quick-question').forEach(button => {
            button.addEventListener('click', (e) => {
                const question = e.target.getAttribute('data-question');
                this.messageInput.value = question;
                this.sendMessage();
            });
        });

        // File upload
        this.uploadButton.addEventListener('click', () => {
            this.fileInput.click();
        });

        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.uploadDocument(e.target.files[0]);
            }
        });

        // Input character counter
        this.messageInput.addEventListener('input', () => {
            const length = this.messageInput.value.length;
            const maxLength = 500;

            if (length > maxLength * 0.9) {
                this.messageInput.style.borderColor = '#f59e0b';
            } else {
                this.messageInput.style.borderColor = '';
            }
        });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Disable input
        this.setInputState(false);

        // Add user message to chat
        this.addMessage(message, 'user');

        // Clear input
        this.messageInput.value = '';

        // Show loading
        this.showLoading(true);

        try {
            const response = await this.queryAPI(message);
            this.addMessage(response.response, 'bot', response.sources);
        } catch (error) {
            console.error('Error:', error);
            this.addMessage(
                'I apologize, but I encountered an error processing your question. Please try again or contact support if the issue persists.',
                'bot'
            );
        } finally {
            this.showLoading(false);
            this.setInputState(true);
            this.messageInput.focus();
        }
    }

    async queryAPI(query) {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    addMessage(text, sender, sources = []) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';

        // Format text with basic HTML support
        textDiv.innerHTML = this.formatMessageText(text);

        contentDiv.appendChild(textDiv);

        // Add sources if available
        if (sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'message-sources';
            sourcesDiv.innerHTML = '<strong>Sources:</strong>';

            sources.forEach(source => {
                const sourceItem = document.createElement('div');
                sourceItem.className = 'source-item';
                sourceItem.textContent = `📄 ${source.source} (Score: ${(source.score * 100).toFixed(1)}%)`;
                sourcesDiv.appendChild(sourceItem);
            });

            contentDiv.appendChild(sourcesDiv);
        }

        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    formatMessageText(text) {
        // Basic text formatting
        text = text.replace(/\n/g, '<br>');

        // Make URLs clickable
        text = text.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
        );

        // Bold text (limited support)
        text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        return text;
    }

    async uploadDocument(file) {
        if (!this.validateFile(file)) {
            alert('Please select a valid file (PDF, DOC, DOCX, or TXT).');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        this.showLoading(true, 'Uploading document...');

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`);
            }

            const result = await response.json();

            this.addMessage(
                `✅ Document "${file.name}" uploaded successfully! Created ${result.chunks_created} text chunks for analysis. You can now ask questions about this document.`,
                'bot'
            );

            // Update document count
            this.checkSystemStatus();

        } catch (error) {
            console.error('Upload error:', error);
            this.addMessage(
                `❌ Failed to upload "${file.name}". Please try again or contact support.`,
                'bot'
            );
        } finally {
            this.showLoading(false);
            this.fileInput.value = ''; // Clear file input
        }
    }

    validateFile(file) {
        const allowedTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ];

        const maxSize = 10 * 1024 * 1024; // 10MB

        return allowedTypes.includes(file.type) && file.size <= maxSize;
    }

    async checkSystemStatus() {
        try {
            const response = await fetch('/api/health');
            const status = await response.json();

            // Update watsonx.ai status
            const watsonxStatus = document.getElementById('watsonxStatus');
            if (watsonxStatus) {
                watsonxStatus.className = `status-dot ${status.watsonx_connected ? 'connected' : 'disconnected'}`;
            }

            // Update document count
            const documentsStatus = document.getElementById('documentsStatus');
            const documentsCount = document.getElementById('documentsCount');
            if (documentsStatus && documentsCount) {
                documentsStatus.className = `status-dot ${status.documents_loaded > 0 ? 'connected' : 'disconnected'}`;
                documentsCount.textContent = `Documents Loaded: ${status.documents_loaded}`;
            }

        } catch (error) {
            console.error('Health check failed:', error);
        }
    }

    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;

        if (enabled) {
            this.messageInput.focus();
        }
    }

    showLoading(show, text = 'Processing your question...') {
        const overlay = this.loadingOverlay;
        const loadingText = overlay.querySelector('.loading-text');

        if (show) {
            loadingText.textContent = text;
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    }

    // Utility method to get formatted timestamp
    getTimestamp() {
        return new Date().toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.collegeAgent = new CollegeAdmissionAgent();

    // Periodic status check (every 30 seconds)
    setInterval(() => {
        window.collegeAgent.checkSystemStatus();
    }, 30000);
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.collegeAgent) {
        window.collegeAgent.checkSystemStatus();
    }
});

// Global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Service worker registration (if available)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
