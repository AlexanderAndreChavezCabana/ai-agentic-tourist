// ============================================
// HUARAZ AI - INTERACTIVE WEB APPLICATION
// ============================================

// Configuration
const CONFIG = {
    API_BASE_URL: window.location.origin,
    WS_URL: `ws://${window.location.host}/ws`,
    SESSION_ID: generateSessionId(),
    RECONNECT_DELAY: 3000,
    MAX_RECONNECT_ATTEMPTS: 5
};

// State Management
const state = {
    ws: null,
    reconnectAttempts: 0,
    isConnected: false,
    currentSession: 'default',
    attractions: [],
    stats: {}
};

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    console.log('🚀 Inicializando Huaraz AI...');
    
    // Initialize components
    initializeParticles();
    initializeHeader();
    initializeTheme();
    initializeChat();
    loadAttractions();
    loadStats();
    initializeEventListeners();
    
    console.log('✅ Aplicación inicializada');
}

// ============================================
// PARTICLES BACKGROUND
// ============================================

function initializeParticles() {
    if (typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: '#667eea' },
                shape: { type: 'circle' },
                opacity: { value: 0.5, random: false },
                size: { value: 3, random: true },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#667eea',
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: 'none',
                    random: false,
                    straight: false,
                    out_mode: 'out',
                    bounce: false
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: { enable: true, mode: 'repulse' },
                    onclick: { enable: true, mode: 'push' },
                    resize: true
                }
            },
            retina_detect: true
        });
    }
}

// ============================================
// HEADER & NAVIGATION
// ============================================

function initializeHeader() {
    const header = document.querySelector('.header');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
    
    // Smooth scroll
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Update active link
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
}

// ============================================
// THEME TOGGLE
// ============================================

function initializeTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    themeToggle.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
}

function updateThemeIcon(theme) {
    const icon = document.querySelector('#themeToggle i');
    icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}

// ============================================
// CHAT FUNCTIONALITY
// ============================================

function initializeChat() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const clearBtn = document.getElementById('clearChatBtn');
    const exportBtn = document.getElementById('exportChatBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    
    // Connect WebSocket
    connectWebSocket();
    
    // Form submission
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessage();
    });
    
    // Enter to send
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Clear chat
    clearBtn.addEventListener('click', clearChat);
    
    // Export chat
    exportBtn.addEventListener('click', exportChat);
    
    // New chat
    newChatBtn.addEventListener('click', () => {
        state.currentSession = generateSessionId();
        clearChat();
        connectWebSocket();
    });
    
    // Quick action buttons
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const message = btn.getAttribute('data-message');
            document.getElementById('messageInput').value = message;
            sendMessage();
        });
    });
}

function connectWebSocket() {
    const wsUrl = `${CONFIG.WS_URL}/${state.currentSession}`;
    console.log(`🔌 Conectando WebSocket: ${wsUrl}`);
    
    try {
        state.ws = new WebSocket(wsUrl);
        
        state.ws.onopen = () => {
            console.log('✅ WebSocket conectado');
            state.isConnected = true;
            state.reconnectAttempts = 0;
            updateConnectionStatus('En línea', true);
        };
        
        state.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleIncomingMessage(data);
        };
        
        state.ws.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
            updateConnectionStatus('Error', false);
        };
        
        state.ws.onclose = () => {
            console.log('🔌 WebSocket cerrado');
            state.isConnected = false;
            updateConnectionStatus('Desconectado', false);
            attemptReconnect();
        };
    } catch (error) {
        console.error('❌ Error al conectar WebSocket:', error);
        // Fallback to HTTP
        console.log('📡 Usando HTTP como fallback');
    }
}

function attemptReconnect() {
    if (state.reconnectAttempts < CONFIG.MAX_RECONNECT_ATTEMPTS) {
        state.reconnectAttempts++;
        console.log(`🔄 Reintentando conexión (${state.reconnectAttempts}/${CONFIG.MAX_RECONNECT_ATTEMPTS})...`);
        
        setTimeout(() => {
            connectWebSocket();
        }, CONFIG.RECONNECT_DELAY);
    } else {
        console.error('❌ Máximo de reintentos alcanzado');
        updateConnectionStatus('Sin conexión', false);
    }
}

function updateConnectionStatus(status, isOnline) {
    const statusElement = document.getElementById('connectionStatus');
    const statusDot = document.querySelector('.status-dot');
    
    if (statusElement) {
        statusElement.textContent = status;
    }
    
    if (statusDot) {
        statusDot.style.background = isOnline ? '#10b981' : '#ef4444';
    }
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    
    // Clear input
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send via WebSocket or HTTP
    if (state.isConnected && state.ws.readyState === WebSocket.OPEN) {
        state.ws.send(JSON.stringify({ message }));
    } else {
        // Fallback to HTTP
        sendMessageHTTP(message);
    }
}

async function sendMessageHTTP(message) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message,
                session_id: state.currentSession
            })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        addMessageToChat('bot', data.response);
    } catch (error) {
        console.error('Error al enviar mensaje:', error);
        hideTypingIndicator();
        addMessageToChat('bot', '❌ Error al procesar tu mensaje. Por favor, intenta de nuevo.');
    }
}

function handleIncomingMessage(data) {
    hideTypingIndicator();
    
    if (data.type === 'bot' || data.type === 'system') {
        addMessageToChat('bot', data.content);
    } else if (data.type === 'error') {
        addMessageToChat('bot', `❌ ${data.content}`);
    }
}

function addMessageToChat(role, content) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const time = new Date().toLocaleTimeString('es-PE', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    // Format content (simple markdown-like)
    const formattedContent = formatMessageContent(content);
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-${role === 'user' ? 'user' : 'robot'}"></i>
        </div>
        <div class="message-content">
            <div class="message-bubble">
                ${formattedContent}
            </div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    
    // Auto-scroll suave al último mensaje - Mejorado
    requestAnimationFrame(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
}

function formatMessageContent(content) {
    // Convert line breaks to <br>
    content = content.replace(/\n/g, '<br>');
    
    // Bold text **text**
    content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text *text*
    content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convertir enlaces HTML (mantener tags <a> intactos)
    // Esto preserva los enlaces tour-link que vienen del backend
    // No hacemos nada aquí porque el contenido ya viene con HTML
    
    // Lists (simple detection)
    if (content.includes('- ') || content.includes('• ')) {
        const lines = content.split('<br>');
        let inList = false;
        let result = [];
        
        for (let line of lines) {
            if (line.trim().startsWith('- ') || line.trim().startsWith('• ')) {
                if (!inList) {
                    result.push('<ul>');
                    inList = true;
                }
                result.push(`<li>${line.replace(/^[•\-]\s*/, '')}</li>`);
            } else {
                if (inList) {
                    result.push('</ul>');
                    inList = false;
                }
                // No envolver en <p> si ya tiene tags HTML
                if (line.includes('<a') || line.includes('<strong>') || line.includes('<em>')) {
                    result.push(line);
                } else {
                    result.push(`<p>${line}</p>`);
                }
            }
        }
        
        if (inList) result.push('</ul>');
        return result.join('');
    }
    
    // Si ya tiene HTML tags, no envolver en <p>
    if (content.includes('<a') || content.includes('<strong>') || content.includes('<em>')) {
        return content;
    }
    
    // Wrap in paragraph
    return `<p>${content}</p>`;
}

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.add('active');
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('active');
    }
}

function clearChat() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.innerHTML = '';
    
    // Add welcome message
    addMessageToChat('bot', `¡Hola! 👋 Soy tu asistente virtual de turismo en Huaraz. 

Puedo ayudarte con:
- 🏔️ Recomendaciones de atracciones
- 📅 Creación de itinerarios
- 🏨 Sugerencias de alojamiento
- 🌤️ Información sobre clima
- ⛰️ Consejos sobre altitud

¿En qué puedo ayudarte hoy?`);
}

function exportChat() {
    const messages = document.querySelectorAll('.message');
    let chatText = 'CONVERSACIÓN - HUARAZ AI\n';
    chatText += '='.repeat(50) + '\n\n';
    
    messages.forEach(msg => {
        const role = msg.classList.contains('user-message') ? 'Usuario' : 'Asistente';
        const content = msg.querySelector('.message-bubble').innerText;
        const time = msg.querySelector('.message-time').innerText;
        
        chatText += `[${time}] ${role}:\n${content}\n\n`;
    });
    
    // Download as text file
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `conversacion-huaraz-${new Date().toISOString().slice(0,10)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// ============================================
// ATTRACTIONS
// ============================================

async function loadAttractions() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/attractions`);
        const data = await response.json();
        state.attractions = data.attractions;
        displayAttractions(state.attractions);
        
        // Update count
        document.getElementById('attractionsCount').textContent = `${data.count}+`;
    } catch (error) {
        console.error('Error al cargar atracciones:', error);
        document.getElementById('attractionsGrid').innerHTML = `
            <div class="loading">
                <i class="fas fa-exclamation-circle"></i>
                <p>Error al cargar atracciones</p>
            </div>
        `;
    }
}

function displayAttractions(attractions) {
    const grid = document.getElementById('attractionsGrid');
    
    if (attractions.length === 0) {
        grid.innerHTML = `
            <div class="loading">
                <i class="fas fa-info-circle"></i>
                <p>No se encontraron atracciones</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = attractions.map(attr => `
        <div class="attraction-card" data-difficulty="${attr.difficulty}">
            <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=200&fit=crop" 
                 alt="${attr.name}" 
                 class="attraction-image"
                 onerror="this.src='https://via.placeholder.com/400x200?text=${encodeURIComponent(attr.name)}'">
            <div class="attraction-content">
                <div class="attraction-header">
                    <h3>${attr.name}</h3>
                    <span class="difficulty-badge difficulty-${attr.difficulty}">
                        ${attr.difficulty}
                    </span>
                </div>
                <p>${attr.description.substring(0, 120)}...</p>
                <div class="attraction-meta">
                    <span><i class="fas fa-mountain"></i> ${attr.altitude}m</span>
                    <span><i class="fas fa-clock"></i> ${attr.duration}</span>
                </div>
            </div>
        </div>
    `).join('');
    
    // Add click handlers
    document.querySelectorAll('.attraction-card').forEach(card => {
        card.addEventListener('click', () => {
            const name = card.querySelector('h3').textContent;
            document.getElementById('messageInput').value = `Cuéntame más sobre ${name}`;
            document.querySelector('#chat').scrollIntoView({ behavior: 'smooth' });
        });
    });
}

// Filter attractions
function initializeEventListeners() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active button
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Filter attractions
            const filter = btn.getAttribute('data-filter');
            filterAttractions(filter);
        });
    });
}

function filterAttractions(difficulty) {
    const cards = document.querySelectorAll('.attraction-card');
    
    cards.forEach(card => {
        if (difficulty === 'all' || card.getAttribute('data-difficulty') === difficulty) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================
// STATISTICS
// ============================================

async function loadStats() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/stats`);
        const data = await response.json();
        state.stats = data;
        updateStatsDisplay(data);
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
    
    // Refresh every 10 seconds
    setTimeout(loadStats, 10000);
}

function updateStatsDisplay(stats) {
    document.getElementById('totalConversations').textContent = stats.total_conversations || 0;
    document.getElementById('totalMessages').textContent = stats.total_messages || 0;
    document.getElementById('activeConnections').textContent = stats.active_connections || 0;
    
    // Update hero stats
    document.getElementById('messagesCount').textContent = `${stats.total_messages || 1000}+`;
    document.getElementById('usersCount').textContent = `${stats.total_conversations || 500}+`;
}

// ============================================
// UTILITIES
// ============================================

function generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substring(7)}`;
}

function showNotification(message, type = 'info') {
    // Simple notification (can be enhanced with a library)
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ============================================
// ANIMATIONS
// ============================================

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.feature-card, .attraction-card, .stats-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ============================================
// ERROR HANDLING
// ============================================

window.addEventListener('error', (event) => {
    console.error('❌ Error global:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('❌ Promise rechazada:', event.reason);
});

// ============================================
// EXPORT
// ============================================

console.log('✅ Huaraz AI JavaScript cargado correctamente');
