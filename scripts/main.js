// API配置
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000',
    ENDPOINTS: {
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream'
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 获取DOM元素
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const suggestionCards = document.getElementById('suggestionCards');
    const historyList = document.getElementById('historyList');
    
    // 禁用发送按钮的默认状态
    sendButton.disabled = true;

    // 发送消息事件处理
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // 监听输入框变化
    messageInput.addEventListener('input', () => {
        sendButton.disabled = !messageInput.value.trim();
    });

    // 发送消息函数
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
    
        // 禁用输入和发送按钮
        messageInput.disabled = true;
        sendButton.disabled = true;
    
        // 添加用户消息到对话区域
        addMessage('user', message);
        messageInput.value = '';
    
        try {
            // 调用后端API获取回复
            const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHAT}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || '请求失败');
            }
    
            // 添加AI回复到对话区域
            addMessage('ai', data.message);
            
            // 处理建议
            if (data.suggestions && data.suggestions.length > 0) {
                data.suggestions.forEach(suggestion => {
                    addSuggestionCard(suggestion);
                });
            }
            
            // 更新历史记录
            updateHistory(message, data.message);
    
        } catch (error) {
            console.error('Error:', error);
            addMessage('error', `发送消息时出现错误：${error.message}`);
        } finally {
            // 重新启用输入和发送按钮
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    }

    // 添加消息到对话区域
    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // 添加建议卡片
    function addSuggestionCard(content) {
        const card = document.createElement('div');
        card.className = 'suggestion-card';
        card.textContent = content;
        suggestionCards.insertBefore(card, suggestionCards.firstChild);
    }

    // 更新历史记录
    function updateHistory(question, answer) {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <strong>问：</strong>${question}<br>
            <strong>答：</strong>${answer}
        `;
        historyList.insertBefore(historyItem, historyList.firstChild);
    }
});