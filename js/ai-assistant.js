class AIAssistant {
    constructor() {
        this.messagesContainer = document.getElementById('ai-messages');
        this.input = document.getElementById('ai-input');
        this.sendButton = document.getElementById('ai-send');
        this.quickActions = document.querySelectorAll('.quick-action');
        
        this.conversationHistory = [];
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadConversationHistory();
    }
    
    setupEventListeners() {
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Quick actions
        this.quickActions.forEach(action => {
            action.addEventListener('click', (e) => {
                const actionType = e.target.getAttribute('data-action');
                this.handleQuickAction(actionType);
            });
        });
        
        // Auto-resize textarea
        this.input.addEventListener('input', () => {
            this.autoResizeTextarea();
        });
    }
    
    autoResizeTextarea() {
        this.input.style.height = 'auto';
        this.input.style.height = Math.min(this.input.scrollHeight, 120) + 'px';
    }
    
    sendMessage() {
        const message = this.input.value.trim();
        if (!message || this.isTyping) return;
        
        this.addMessage(message, 'user');
        this.input.value = '';
        this.autoResizeTextarea();
        
        // Simulate AI thinking
        this.showTypingIndicator();
        
        // Generate AI response after delay
        setTimeout(() => {
            this.removeTypingIndicator();
            this.generateAIResponse(message);
        }, 1000 + Math.random() * 1000); // Random delay for realism
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `d-flex mb-3 ${sender === 'user' ? 'justify-content-end' : ''}`;
        
        const messageBubble = document.createElement('div');
        messageBubble.className = `message-bubble ${sender === 'user' ? 'user-message bg-primary text-white' : 'ai-message bg-light text-dark'}`;
        messageBubble.style.maxWidth = '70%';
        messageBubble.innerHTML = `
            <div class="p-3 rounded">
                <p class="mb-0">${this.escapeHtml(content)}</p>
            </div>
        `;
        
        if (sender === 'ai') {
            const avatar = document.createElement('div');
            avatar.className = 'flex-shrink-0 me-2';
            avatar.innerHTML = '<i class="bi bi-robot text-primary fs-5"></i>';
            messageDiv.appendChild(avatar);
        }
        
        messageDiv.appendChild(messageBubble);
        
        if (sender === 'user') {
            const avatar = document.createElement('div');
            avatar.className = 'flex-shrink-0 ms-2';
            avatar.innerHTML = '<i class="bi bi-person-circle text-secondary fs-5"></i>';
            messageDiv.appendChild(avatar);
        }
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Save to conversation history
        this.conversationHistory.push({
            sender: sender,
            content: content,
            timestamp: new Date().toISOString()
        });
        
        this.saveConversationHistory();
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'd-flex mb-3 typing-indicator';
        typingDiv.innerHTML = `
            <div class="flex-shrink-0 me-2">
                <i class="bi bi-robot text-primary fs-5"></i>
            </div>
            <div class="bg-light text-dark p-3 rounded" style="max-width: 70%">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    removeTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = this.messagesContainer.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    generateAIResponse(userMessage) {
        let response = '';
        const lowerMessage = userMessage.toLowerCase();
        
        // Basic intent detection
        if (lowerMessage.includes('buy') || lowerMessage.includes('purchase') || lowerMessage.includes('shop')) {
            response = this.generateBuyResponse(lowerMessage);
        } else if (lowerMessage.includes('sell') || lowerMessage.includes('price') || lowerMessage.includes('value')) {
            response = this.generateSellResponse(lowerMessage);
        } else if (lowerMessage.includes('repair') || lowerMessage.includes('fix') || lowerMessage.includes('broken')) {
            response = this.generateRepairResponse(lowerMessage);
        } else if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
            response = "Hello! I'm your ElectroFix AI assistant. I can help you with buying, selling, or repairing devices. What would you like to know?";
        } else {
            response = "I understand you're interested in our services. I can help you with:\n\n• Finding the perfect device to buy\n• Estimating the value of your used device\n• Getting repair cost estimates\n\nWhat would you like assistance with today?";
        }
        
        this.addMessage(response, 'ai');
    }
    
    generateBuyResponse(message) {
        const responses = [
            "I can help you find the perfect device! What type of device are you looking for (phone, laptop, tablet)?",
            "Great choice! We have certified pre-owned devices with warranty. What's your budget range?",
            "I'd be happy to help you find a device. Are you looking for any specific brand or features?",
            "We have excellent options available. Could you tell me what you'll primarily use the device for?"
        ];
        
        if (message.includes('phone') || message.includes('iphone') || message.includes('samsung')) {
            return "For smartphones, I recommend checking our certified pre-owned iPhones and Samsung Galaxy devices. They come with 1-year warranty and are thoroughly tested. What's your budget?";
        } else if (message.includes('laptop') || message.includes('macbook') || message.includes('dell')) {
            return "We have a great selection of laptops from Apple, Dell, and HP. Are you looking for something for work, gaming, or general use?";
        } else if (message.includes('tablet') || message.includes('ipad')) {
            return "Our tablet collection includes iPads and Samsung Galaxy Tabs perfect for work or entertainment. What screen size are you considering?";
        }
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    generateSellResponse(message) {
        const responses = [
            "I can help estimate your device's value! What device do you want to sell and what's its condition?",
            "Great! To give you an accurate price estimate, I'll need to know the device type, model, and condition.",
            "I can provide a valuation for your device. Could you tell me the brand, model, and overall condition?",
            "Let me help you get the best price for your device. What are you looking to sell?"
        ];
        
        if (message.includes('iphone') || message.includes('apple')) {
            return "Apple devices typically hold their value well! For an accurate estimate, I'd need to know the model, storage capacity, and condition. Recent iPhones in good condition can get 60-80% of their original price.";
        } else if (message.includes('samsung')) {
            return "Samsung devices are popular in the used market! The value depends on the model, age, and condition. Flagship models like the Galaxy S series retain good value.";
        }
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    generateRepairResponse(message) {
        const responses = [
            "I can help with repair estimates! What device needs repair and what's the issue?",
            "Let me help you with repair options. Could you describe the device and the problem you're experiencing?",
            "I can provide repair cost estimates. What type of device is it and what seems to be wrong?",
            "Our repair services come with 90-day warranty. Tell me about your device and the issue."
        ];
        
        if (message.includes('screen') || message.includes('crack')) {
            return "Screen replacements are common repairs. For smartphones, it typically costs $50-$150 depending on the model. For laptops, it can range from $100-$300.";
        } else if (message.includes('battery') || message.includes('charge')) {
            return "Battery replacements usually cost $40-$80 for phones and $80-$150 for laptops, including parts and labor with 90-day warranty.";
        } else if (message.includes('water') || message.includes('liquid')) {
            return "Water damage repairs can be complex. We offer free diagnostics to assess the damage. Costs typically range from $80-$200 depending on the extent of damage.";
        }
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    handleQuickAction(actionType) {
        let message = '';
        
        switch(actionType) {
            case 'price-estimate':
                message = "I'd like to get a price estimate for my device";
                break;
            case 'find-device':
                message = "I want to find a device to buy";
                break;
            case 'repair-cost':
                message = "I need a repair cost estimate";
                break;
        }
        
        this.addMessage(message, 'user');
        this.showTypingIndicator();
        
        setTimeout(() => {
            this.removeTypingIndicator();
            this.generateAIResponse(message);
        }, 1000);
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    saveConversationHistory() {
        // Keep only last 50 messages to prevent storage overflow
        if (this.conversationHistory.length > 50) {
            this.conversationHistory = this.conversationHistory.slice(-50);
        }
        
        try {
            localStorage.setItem('electrofix-ai-conversation', JSON.stringify(this.conversationHistory));
        } catch (e) {
            console.warn('Could not save conversation history:', e);
        }
    }
    
    loadConversationHistory() {
        try {
            const saved = localStorage.getItem('electrofix-ai-conversation');
            if (saved) {
                this.conversationHistory = JSON.parse(saved);
                
                // Clear current messages and reload history
                this.messagesContainer.innerHTML = '';
                this.conversationHistory.forEach(msg => {
                    this.addMessage(msg.content, msg.sender);
                });
            }
        } catch (e) {
            console.warn('Could not load conversation history:', e);
        }
    }
    
    clearConversation() {
        this.conversationHistory = [];
        this.messagesContainer.innerHTML = '';
        localStorage.removeItem('electrofix-ai-conversation');
        
        // Add welcome message
        this.addMessage("Hello! I can help you find the perfect device or estimate prices. What are you looking for?", 'ai');
    }
    
    // Export conversation for support
    exportConversation() {
        const conversationText = this.conversationHistory.map(msg => 
            `${msg.sender === 'user' ? 'You' : 'AI'}: ${msg.content}`
        ).join('\n\n');
        
        const blob = new Blob([conversationText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `electrofix-conversation-${new Date().toISOString().split('T')[0]}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Add some CSS for typing animation
const style = document.createElement('style');
style.textContent = `
    .typing-dots {
        display: inline-flex;
        gap: 2px;
    }
    
    .typing-dots span {
        height: 6px;
        width: 6px;
        border-radius: 50%;
        background-color: #6c757d;
        animation: typing-dot 1.4s ease-in-out infinite both;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing-dot {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    .message-bubble {
        border-radius: 18px;
        word-wrap: break-word;
    }
    
    .user-message {
        border-bottom-right-radius: 4px;
    }
    
    .ai-message {
        border-bottom-left-radius: 4px;
    }
`;
document.head.appendChild(style);

// Initialize AI Assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiAssistant = new AIAssistant();
});