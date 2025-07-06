<template>
  <div class="chatbot-container">
    <!-- Chatbot Toggle Button -->
    <button 
      @click="toggleChatbot" 
      class="chatbot-toggle"
      :class="{ 'active': isOpen }"
      title="Chat with AI Assistant"
    >
      <svg v-if="!isOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H6L4 18V4H20V16Z" fill="currentColor"/>
        <path d="M7 9H17V11H7V9ZM7 12H14V14H7V12Z" fill="currentColor"/>
      </svg>
      <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
      </svg>
    </button>

    <!-- Chatbot Window -->
    <div v-if="isOpen" class="chatbot-window">
      <!-- Header -->
      <div class="chatbot-header">
        <div class="chatbot-title">
          <div class="chatbot-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4S20 7.58 20 12S16.42 20 12 20Z" fill="currentColor"/>
              <path d="M12 6C9.79 6 8 7.79 8 10C8 12.21 9.79 14 12 14C14.21 14 16 12.21 16 10C16 7.79 14.21 6 12 6ZM12 12C10.9 12 10 11.1 10 10C10 8.9 10.9 8 12 8C13.1 8 14 8.9 14 10C14 11.1 13.1 12 12 12Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="chatbot-info">
            <h3>AI Assistant</h3>
            <span class="status" :class="{ 'online': isOnline }">
              {{ isOnline ? 'Online' : 'Offline' }}
            </span>
          </div>
        </div>
        <button @click="toggleChatbot" class="close-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
          </svg>
        </button>
      </div>

      <!-- Messages Container -->
      <div class="messages-container" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4S20 7.58 20 12S16.42 20 12 20Z" fill="currentColor"/>
              <path d="M12 6C9.79 6 8 7.79 8 10C8 12.21 9.79 14 12 14C14.21 14 16 12.21 16 10C16 7.79 14.21 6 12 6ZM12 12C10.9 12 10 11.1 10 10C10 8.9 10.9 8 12 8C13.1 8 14 8.9 14 10C14 11.1 13.1 12 12 12Z" fill="currentColor"/>
            </svg>
          </div>
          <h3>Hello! 👋</h3>
          <p>I'm your AI assistant powered by ChatGPT. How can I help you today?</p>
          <div class="ai-status">
            <span class="ai-badge">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L13.09 8.26L20 9L13.09 9.74L12 16L10.91 9.74L4 9L10.91 8.26L12 2Z" fill="currentColor"/>
              </svg>
              AI Powered
            </span>
          </div>
          <div class="quick-actions">
            <button @click="sendQuickMessage('How do I take a quiz?')" class="quick-action-btn">
              How do I take a quiz?
            </button>
            <button @click="sendQuickMessage('View my quiz results')" class="quick-action-btn">
              View my results
            </button>
            <button @click="sendQuickMessage('Study tips')" class="quick-action-btn">
              Study tips
            </button>
            <button @click="sendQuickMessage('Ask me anything!')" class="quick-action-btn ai-question">
              🤖 Ask me anything!
            </button>
          </div>
        </div>

        <div v-for="(message, index) in messages" :key="index" class="message" :class="message.type">
          <div class="message-avatar" v-if="message.type === 'bot'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4S20 7.58 20 12S16.42 20 12 20Z" fill="currentColor"/>
              <path d="M12 6C9.79 6 8 7.79 8 10C8 12.21 9.79 14 12 14C14.21 14 16 12.21 16 10C16 7.79 14.21 6 12 6ZM12 12C10.9 12 10 11.1 10 10C10 8.9 10.9 8 12 8C13.1 8 14 8.9 14 10C14 11.1 13.1 12 12 12Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.text)"></div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
          <div class="message-avatar user-avatar" v-if="message.type === 'user'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" fill="currentColor"/>
            </svg>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="message bot">
          <div class="message-avatar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12S6.47 22 11.99 22C17.52 22 22 17.52 22 12S17.52 2 11.99 2ZM12 20C7.58 20 4 16.42 4 12S7.58 4 12 4S20 7.58 20 12S16.42 20 12 20Z" fill="currentColor"/>
              <path d="M12 6C9.79 6 8 7.79 8 10C8 12.21 9.79 14 12 14C14.21 14 16 12.21 16 10C16 7.79 14.21 6 12 6ZM12 12C10.9 12 10 11.1 10 10C10 8.9 10.9 8 12 8C13.1 8 14 8.9 14 10C14 11.1 13.1 12 12 12Z" fill="currentColor"/>
            </svg>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="input-area">
        <div class="input-container">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="Type your message..."
            class="message-input"
            :disabled="isTyping"
          />
          <button 
            @click="sendMessage" 
            class="send-btn"
            :disabled="!userInput.trim() || isTyping"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import { sendChatMessage } from '../api';

// Reactive data
const isOpen = ref(false);
const isOnline = ref(true);
const isTyping = ref(false);
const messages = ref([]);
const userInput = ref('');
const messagesContainer = ref(null);

// Methods
const toggleChatbot = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    nextTick(() => {
      scrollToBottom();
    });
  }
};

const sendMessage = async () => {
  const message = userInput.value.trim();
  if (!message || isTyping.value) return;

  // Add user message
  addMessage(message, 'user');
  userInput.value = '';
  isTyping.value = true;

  try {
    // Send to backend
    const response = await sendChatMessage(message);
    addMessage(response.message, 'bot');
  } catch (error) {
    console.error('Error sending message:', error);
    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
  } finally {
    isTyping.value = false;
  }
};

const sendQuickMessage = (message) => {
  userInput.value = message;
  sendMessage();
};

const addMessage = (text, type) => {
  messages.value.push({
    text,
    type,
    timestamp: new Date()
  });
  
  nextTick(() => {
    scrollToBottom();
  });
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const formatMessage = (text) => {
  // Convert URLs to clickable links
  return text.replace(
    /(https?:\/\/[^\s]+)/g,
    '<a href="$1" target="_blank" class="message-link">$1</a>'
  );
};

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

// Watch for new messages to auto-scroll
watch(messages, () => {
  nextTick(() => {
    scrollToBottom();
  });
});

onMounted(() => {
  // Initialize with welcome message if needed
});
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.chatbot-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chatbot-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
}

.chatbot-toggle.active {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.chatbot-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 380px;
  height: 500px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #e0e0e0;
}

.chatbot-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chatbot-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chatbot-avatar {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chatbot-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.status {
  font-size: 12px;
  opacity: 0.8;
}

.status.online {
  color: #4ade80;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.messages-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #f8f9fa;
}

.welcome-message {
  text-align: center;
  padding: 20px 0;
}

.welcome-icon {
  margin-bottom: 16px;
  color: #667eea;
}

.welcome-message h3 {
  margin: 0 0 8px 0;
  color: #1a1a1a;
  font-size: 18px;
}

.welcome-message p {
  margin: 0 0 20px 0;
  color: #666;
  font-size: 14px;
}

.ai-status {
  margin-bottom: 20px;
}

.ai-badge {
  background: #667eea;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
  color: white;
  display: flex;
  align-items: center;
  gap: 4px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-action-btn {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 13px;
  color: #1a1a1a;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.quick-action-btn:hover {
  background: #f0f0f0;
  border-color: #667eea;
}

.quick-action-btn.ai-question {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.quick-action-btn.ai-question:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: translateY(-1px);
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 16px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.user-avatar {
  background: #10b981;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  text-align: right;
}

.message-text {
  background: white;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.4;
  color: #1a1a1a;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
}

.message.user .message-text {
  background: #667eea;
  color: white;
}

.message-time {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  padding: 0 4px;
}

.message.user .message-time {
  text-align: right;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: white;
  border-radius: 18px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.input-area {
  padding: 16px 20px;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 24px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.message-input:focus {
  border-color: #667eea;
}

.message-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.send-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #667eea;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  background: #5a6fd8;
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.message-link {
  color: #667eea;
  text-decoration: none;
}

.message-link:hover {
  text-decoration: underline;
}

/* Scrollbar styling */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Responsive design */
@media (max-width: 480px) {
  .chatbot-window {
    width: calc(100vw - 40px);
    height: 60vh;
    bottom: 80px;
    right: 20px;
  }
  
  .chatbot-container {
    bottom: 10px;
    right: 10px;
  }
}
</style> 