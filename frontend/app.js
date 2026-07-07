/**
 * app.js — Shared utilities for WatchQueue frontend.
 * 
 * Provides: API client, auth management, toast notifications,
 * navigation, and common helpers.
 */

const API_BASE = '/api';

// ── Auth Management ─────────────────────────────────────────
const Auth = {
    getToken() { return localStorage.getItem('wq_token'); },
    setToken(token) { localStorage.setItem('wq_token', token); },
    getUser() { 
        const u = localStorage.getItem('wq_user');
        return u ? JSON.parse(u) : null;
    },
    setUser(user) { localStorage.setItem('wq_user', JSON.stringify(user)); },
    logout() {
        localStorage.removeItem('wq_token');
        localStorage.removeItem('wq_user');
        window.location.href = '/';
    },
    isLoggedIn() { return !!this.getToken(); },
    requireAuth() {
        if (!this.isLoggedIn()) {
            window.location.href = '/';
            return false;
        }
        return true;
    },
};

// ── API Client ──────────────────────────────────────────────
async function api(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = options.headers || {};
    
    if (Auth.getToken()) {
        headers['Authorization'] = `Bearer ${Auth.getToken()}`;
    }
    
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }
    
    try {
        const response = await fetch(url, { ...options, headers });
        
        if (response.status === 401) {
            Auth.logout();
            return null;
        }
        
        if (!response.ok) {
            let detail = 'Something went wrong';
            try {
                const errJson = await response.json();
                detail = errJson.detail || detail;
                if (Array.isArray(detail)) {
                    detail = detail[0].msg; // Handle pydantic validation errors
                }
            } catch (e) {}
            throw new Error(detail);
        }
        
        if (response.status === 204) return null;
        return response.json();
    } catch (e) {
        console.error('API Error:', e);
        throw e;
    }
}

// ── Toast Notifications ─────────────────────────────────────
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span style="font-weight:bold">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
        <span>${message}</span>
    `;
    container.appendChild(toast);
    
    // Trigger reflow
    toast.offsetHeight;
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const c = document.createElement('div');
    c.id = 'toast-container';
    document.body.appendChild(c);
    return c;
}

// ── Navigation ──────────────────────────────────────────────
function renderNav(activePage) {
    const nav = document.getElementById('nav-sidebar');
    if (!nav) return;
    const user = Auth.getUser();
    const links = [
        { href: '/dashboard.html', icon: '📊', label: 'Dashboard', id: 'dashboard' },
        { href: '/todos.html', icon: '📝', label: 'To-Do & Media', id: 'todos' },
        { href: '/education.html', icon: '📚', label: 'Education Hub', id: 'education' },
        { href: '/timetable.html', icon: '📅', label: 'Timetable', id: 'timetable' },
        { href: '/attendance.html', icon: '✅', label: 'Attendance', id: 'attendance' },
    ];
    
    let html = `
        <div class="nav-brand">
            <span class="nav-logo">🎬</span>
            <span class="nav-title">WatchQueue</span>
        </div>
        <div class="nav-links">
    `;
    
    links.forEach(l => {
        html += `
            <a href="${l.href}" class="nav-link ${activePage === l.id ? 'active' : ''}">
                <span>${l.icon}</span>
                <span>${l.label}</span>
            </a>
        `;
    });
    
    html += `
        </div>
        <div class="nav-footer">
            <div class="nav-user">
                <div class="nav-avatar">${user?.username?.[0]?.toUpperCase() || '?'}</div>
                <span>${user?.username || 'User'}</span>
            </div>
            <button class="btn btn-ghost" onclick="Auth.logout()" style="width:100%">Logout</button>
        </div>
    `;
    
    nav.innerHTML = html;
}

// ── Helpers ─────────────────────────────────────────────────
function formatDuration(seconds) {
    if (!seconds) return '';
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function getPriorityColor(score) {
    if (score <= 3) return 'var(--priority-low)';
    if (score <= 6) return 'var(--priority-medium)';
    if (score <= 9) return 'var(--priority-high)';
    return 'var(--priority-critical)';
}

function getCategoryIcon(category) {
    const icons = { movie: '🎬', education: '📚', entertainment: '🎮', book: '📖', podcast: '🎙️', article: '📰', other: '📦' };
    return icons[category] || '📦';
}

function getPlatformIcon(platform) {
    const icons = { youtube: '▶️', netflix: '🎬', instagram: '📸', prime_video: '🎥', disney_plus: '✨', hotstar: '⭐', other: '🔗' };
    return icons[platform] || '🔗';
}

function debounce(fn, ms = 300) {
    let timer;
    return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}
