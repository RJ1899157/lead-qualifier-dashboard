// components.js

// 1. DYNAMIC SIDEBAR WITH ANIMATED HAMBURGER ICON
const style = document.createElement('style');
const isAnalyticsPage = window.location.pathname.includes('analytics');
style.textContent = `
  app-sidebar { display: block; width: 240px; height: 100vh; flex-shrink: 0; background: #1e293b; border-right: 1px solid #334155; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; }
  .sidebar { width: 240px; height: 100%; padding: 24px 16px; display: flex; flex-direction: column; gap: 8px; }

  .nav-item { padding: 10px 12px; border-radius: 10px; cursor: pointer; font-size: 14px; color: #cbd5e1; text-decoration: none; font-weight: 600; letter-spacing: 0.02em; transition: all 0.15s ease; display: block; }
  .nav-item:hover:not(.active) { background: #334155; color: #f8fafc; transform: translateX(1px); }
  .nav-item.active { background: #6366f1; color: #fff; box-shadow: 0 10px 25px rgba(99,102,241,0.2); }
  
  body.sidebar-hidden app-sidebar { width: 0px !important; border-right: none; }
  body.sidebar-hidden .main { flex: 1; }
  app-chatbot { display: contents; }

  .sidebar-toggle-btn, .topbar-hamburger { background: transparent; border: none; cursor: pointer; width: 32px; height: 32px; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 4px; padding: 4px; border-radius: 6px; transition: background 0.15s ease; flex-shrink: 0; }
  .sidebar-toggle-btn:hover, .topbar-hamburger:hover { background: #334155; }
  .sidebar-toggle-btn .bar, .topbar-hamburger .bar { display: block; width: 18px; height: 2px; background: #94a3b8; border-radius: 2px; }

  body:not(.sidebar-hidden) .sidebar-toggle-btn .bar:nth-child(1) { transform: translateY(6px) rotate(45deg); }
  body:not(.sidebar-hidden) .sidebar-toggle-btn .bar:nth-child(2) { opacity: 0; }
  body:not(.sidebar-hidden) .sidebar-toggle-btn .bar:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }

  .topbar-hamburger { display: none; }
  body.sidebar-hidden .topbar-hamburger { display: flex; }
  body.sidebar-hidden .topbar-hamburger .bar:nth-child(1) { transform: translateY(0) rotate(0deg); }
  body.sidebar-hidden .topbar-hamburger .bar:nth-child(2) { opacity: 1; }
  body.sidebar-hidden .topbar-hamburger .bar:nth-child(3) { transform: translateY(0) rotate(0deg); }

  .chat-toggle { position: fixed; bottom: 28px; right: 28px; width: 55px; height: 55px; background: #158d93; border-radius: 50%; border: none; cursor: pointer; color: #fff; box-shadow: 0 4px 20px rgba(99,102,241,0.4); z-index: 200; display: inline-flex; align-items: center; justify-content: center; }
  .chat-toggle i { font-size: 26px; display: inline-block; line-height: 1; transform: translateY(2px); }
  .icon-button img, .icon-button svg { width: 20px; height: 20px; display: block; }
  
  .chat-window { position: fixed; bottom: 92px; right: 28px; width: 380px; height: 500px; background: #1e293b; border: 1px solid #334155; border-radius: 16px; flex-direction: column; z-index: 200; box-shadow: 0 8px 40px rgba(0,0,0,0.4); display: none; }
  .chat-window.open { display: flex; }
  
  .chat-header { padding: 8px 18px; border-bottom: 1px solid #334155; display: flex; align-items: center; justify-content: space-between; }
  .chat-header-left { display: flex; align-items: center; gap: 10px; }
  .chat-avatar { width: 38px; height: 38px; background: #158d93; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; }
  .chat-header-title { font-size: 13px; font-weight: 600; color: #f8fafc; }
  .chat-header-sub { font-size: 11px; color: #64748b; }
  
  .chat-reset { background: transparent; border: none; color: #64748b; cursor: pointer; font-size: 11px; }
  .chat-reset:hover { color: #94a3b8; }
  
  .chat-messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
  .chat-msg { max-width: 85%; padding: 10px 13px; border-radius: 12px; font-size: 12.5px; line-height: 1.6; }
  .chat-msg.user { background: #6366f1; color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
  .chat-msg.agent { background: #0f172a; color: #e2e8f0; align-self: flex-start; border-bottom-left-radius: 4px; }
  .chat-msg.typing { color: #64748b; font-style: italic; }
  
  .chat-input-area { padding: 12px; border-top: 1px solid #334155; display: flex; gap: 8px; }
  .chat-input { flex: 1; background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 9px 12px; color: #e2e8f0; font-size: 12.5px; font-family: inherit; }
  .chat-input:focus { outline: none; border-color: #6366f1; }
  
  .chat-send { background: transparent; border: none; color: #e2e8f0; width: 34px; height: 34px; border-radius: 50%; cursor: pointer; font-size: 14px; display: inline-flex; align-items: center; justify-content: center; transition: all 0.15s ease; }
  .chat-send i { font-size: 15px; display: inline-block; line-height: 1; transform: translateY(2px); }
  .chat-send:hover { color: #64748b; }

  .chat-suggestions { display: flex; flex-wrap: wrap; gap: 6px; padding: 0 16px 12px; }
  .suggestion-chip { background: #0f172a; border: 1px solid #334155; border-radius: 20px; padding: 5px 10px; font-size: 11px; color: #94a3b8; cursor: pointer; }
  .suggestion-chip:hover { border-color: #6366f1; color: #6366f1; }
`;
document.head.appendChild(style);

class AppSidebar extends HTMLElement {
  connectedCallback() {
    const activeTab = this.getAttribute('active') || 'dashboard';

    const filterSection = isAnalyticsPage ? '' : `
      <hr style="border: none; border-top: 1px solid #334155; margin: 16px 0; padding: 0 4px;">
      
      <!-- SEARCH INPUT ELEMENT -->
      <div style="display: flex; flex-direction: column; gap: 8px; padding: 0 12px 12px;">
        <label for="sidebar-search" style="font-size: 13px; color: #f8fafc; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Search Leads:</label>
        <div style="position: relative; display: flex; align-items: center;">
          <input id="sidebar-search" type="text" placeholder="Type name, company..." oninput="typeof handleSidebarSearch==='function'&&handleSidebarSearch(this.value)" style="width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 8px 10px; padding-left: 32px; color: #e2e8f0; font-size: 13px; font-family: inherit; outline: none;">
          <i class="fi fi-sr-search" style="position: absolute; left: 10px; color: #475569; font-size: 13px; display: flex; align-items: center; pointer-events: none;"></i>
        </div>
      </div>

      <!-- FILTER CATEGORY SELECTOR -->
      <div style="display: flex; flex-direction: column; gap: 8px; padding: 0 12px 8px;">
        <label for="sidebar-filter-category" style="font-size: 13px; color: #f8fafc; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Filter by:</label>
        <select id="sidebar-filter-category" onchange="typeof changeFilterCategory==='function'&&changeFilterCategory(this.value)" style="width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 8px 10px; color: #e2e8f0; font-size: 13px; font-family: inherit; outline: none; cursor: pointer;">
          <option value="status">Status</option>
          <option value="industry">Industry</option>
          <option value="country">Country</option>
        </select>
      </div>

      <div id="sidebar-sub-options" style="display: flex; flex-direction: column; gap: 4px; padding: 0 4px 12px;">
        </div>

      <hr style="border: none; border-top: 1px solid #334155; margin: 4px 0 16px; padding: 0 4px;">

      <div style="display: flex; flex-direction: column; gap: 8px; padding: 0 12px;">
        <label for="sidebar-sort-select" style="font-size: 13px; color: #f8fafc; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Sort by:</label>
        <select id="sidebar-sort-select" onchange="typeof handleSidebarSort==='function'&&handleSidebarSort(this.value)" style="width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 8px 10px; color: #e2e8f0; font-size: 13px; font-family: inherit; outline: none; cursor: pointer;">
          <option value="none" selected disabled>Select ordering...</option>
          <option value="name-asc">Name (A-Z)</option>
          <option value="name-desc">Name (Z-A)</option>
          <option value="score-asc">Score (Low to High)</option>
          <option value="score-desc">Score (High to Low)</option>
        </select>
      </div>
    `;
    this.innerHTML = `
      <div class="sidebar">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;padding:0 8px;">
          <div style="font-size:18px;font-weight:700;color:#f8fafc;">Lead<span style="color:#6366f1">AI</span></div>
          <button class="sidebar-toggle-btn" onclick="toggleSidebar()" aria-label="Toggle sidebar">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
          </button>
        </div>
        <a href="/" id="dashboard-tab" class="nav-item ${activeTab === 'dashboard' ? 'active' : ''}">Dashboard</a>
        <a href="/sales-assistant" id="sales-tab" class="nav-item ${activeTab === 'sales' ? 'active' : ''}">Sales Assistant</a>
        <a href="/analytics" id="analytics-tab" class="nav-item ${activeTab === 'analytics' ? 'active' : ''}">Analytics</a>
        
        ${filterSection}
      </div>
    `;
  }
}

class AppChatbot extends HTMLElement {
  connectedCallback() {
    requestAnimationFrame(() => {
      const topbar = document.querySelector('.topbar');
      if (topbar && !topbar.querySelector('.topbar-hamburger')) {
        const btn = document.createElement('button');
        btn.className = 'topbar-hamburger';
        btn.setAttribute('aria-label', 'Toggle sidebar');
        btn.setAttribute('onclick', 'toggleSidebar()');
        btn.innerHTML = `<span class="bar"></span><span class="bar"></span><span class="bar"></span>`;
        topbar.insertBefore(btn, topbar.firstChild);
      }
    });

    this.innerHTML = `
      <button class="chat-toggle icon-button" onclick="toggleChat()" aria-label="Open chat">
        <i class="fi fi-sr-chatbot"></i>
      </button>
      <div class="chat-window" id="chat-window">
        <div class="chat-header">
          <div class="chat-header-left">
            <div class="chat-avatar"><i class="fi fi-sr-user-robot"></i></div>
            <div>
              <div class="chat-header-title">Sales AI Assistant</div>
              <div class="chat-header-sub">Ask anything about your leads</div>
            </div>
          </div>
          <button class="chat-reset" onclick="resetChat()">Reset chat</button>
        </div>
        <div class="chat-messages" id="chat-messages">
          <div class="chat-msg agent">Hi! I'm your Sales AI Assistant. Ask me anything about leads, pitches, emails or sales strategy.</div>
        </div>
        <div class="chat-suggestions" id="suggestions">
          <div class="suggestion-chip" onclick="sendSuggestion(this)">Who should I call first?</div>
          <div class="suggestion-chip" onclick="sendSuggestion(this)">Draft email for top lead</div>
          <div class="suggestion-chip" onclick="sendSuggestion(this)">What objections might I face?</div>
        </div>
        <div class="chat-input-area">
          <input class="chat-input" id="chat-input" type="text" placeholder="Ask about your leads..." onkeydown="if(event.key==='Enter') sendChat()">
          <button class="chat-send icon-button" onclick="sendChat()" aria-label="Send message"><i class="fi fi-sr-paper-plane-top"></i></button>
        </div>
      </div>
    `;
  }
}

customElements.define('app-sidebar', AppSidebar);
customElements.define('app-chatbot', AppChatbot);

// Clean Sanitation Pipeline preventing Double-Encoding Issues
window.safeHTML = function(text) {
  if (text == null) return '';
  const div = document.createElement('div');
  div.textContent = String(text);
  return div.innerHTML;
};

window.htmlEncode = function(text) {
  return window.safeHTML(text).replace(/\n/g, '<br>');
};

window.toggleChat = function() {
  document.getElementById('chat-window').classList.toggle('open');
};

window.toggleSidebar = function() {
  const hidden = document.body.classList.toggle('sidebar-hidden');
  localStorage.setItem('sidebarHidden', hidden ? 'true' : 'false');
};

window.restoreSidebarState = function() {
  const hidden = localStorage.getItem('sidebarHidden') === 'true';
  if (hidden) document.body.classList.add('sidebar-hidden');
};

window.sendChat = async function() {
  const input = document.getElementById('chat-input');
  const message = input.value.trim();
  if (!message) return;
  input.value = '';
  document.getElementById('suggestions').style.display = 'none';
  appendMessage(message, 'user');
  appendMessage('Thinking...', 'agent typing', 'typing-msg');
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  const data = await res.json();
  document.getElementById('typing-msg')?.remove();
  appendMessage(data.response, 'agent');
};

window.sendSuggestion = function(el) {
  document.getElementById('chat-input').value = el.textContent;
  sendChat();
};

window.appendMessage = function(text, type, id = '') {
  const messages = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = `chat-msg ${type}`;
  if (id) div.id = id;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
};

window.resetChat = async function() {
  await fetch('/api/chat/reset', { method: 'POST' });
  const messages = document.getElementById('chat-messages');
  messages.innerHTML = '<div class="chat-msg agent">Chat reset. Ask me anything about your leads!</div>';
  document.getElementById('suggestions').style.display = 'flex';
};

window.changeFilterCategory = function(category) {
  if (typeof handleCategoryChange === 'function') {
    handleCategoryChange(category);
  }
};

window.handleSidebarSort = function(sortToken) {
  if (typeof sortLeads === 'function') {
    sortLeads(sortToken);
  }
};

window.renderSidebarSubButtons = function(options, activeValue, clickFuncName) {
  const container = document.getElementById('sidebar-sub-options');
  if (!container) return;
  
  container.innerHTML = options.map(opt => {
    const isActive = opt.value === activeValue;
    let dotHtml = '';
    
    if (opt.value === 'Hot') dotHtml = '<div style="width:8px;height:8px;border-radius:50%;background:#ef4444"></div>';
    else if (opt.value === 'Warm') dotHtml = '<div style="width:8px;height:8px;border-radius:50%;background:#f59e0b"></div>';
    else if (opt.value === 'Cold') dotHtml = '<div style="width:8px;height:8px;border-radius:50%;background:#3b82f6"></div>';
    else if (opt.value === 'all') dotHtml = '<div style="width:8px;height:8px;border-radius:50%;background:#6366f1"></div>';
    else dotHtml = '<div style="width:6px;height:6px;border-radius:50%;background:#94a3b8"></div>';

    return `
      <div class="filter-btn ${isActive ? 'active' : ''}" onclick="window.${clickFuncName}('${opt.value}', this)" style="padding:8px 12px;border-radius:8px;cursor:pointer;font-size:13px;display:flex;align-items:center;gap:8px;color:${isActive ? '#f8fafc' : '#94a3b8'}; background: ${isActive ? '#334155' : 'transparent'};">
        ${dotHtml} ${opt.label}
      </div>
    `;
  }).join('');
};

window.handleSidebarSearch = function(query) {
  if (typeof searchLeads === 'function') {
    searchLeads(query);
  }
};