// DOM Elements
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const resultsContainer = document.getElementById('resultsContainer');
const resultsCount = document.getElementById('resultsCount');
const searchQuery = document.getElementById('searchQuery');
const noResults = document.getElementById('noResults');
const suggestionTags = document.querySelectorAll('.suggestion-tag');
const totalDocs = document.getElementById('totalDocs');
const vocabSize = document.getElementById('vocabSize');

// API Base URL
const API_BASE_URL = '/api';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Search form submission
    searchForm.addEventListener('submit', handleSearch);
    
    // Suggestion tags
    suggestionTags.forEach(tag => {
        tag.addEventListener('click', function() {
            const query = this.getAttribute('data-query');
            searchInput.value = query;
            performSearch(query);
        });
    });
    
    // Enter key in search input
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleSearch(e);
        }
    });
}

// Handle search form submission
function handleSearch(e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    
    if (!query) {
        alert('Vui lòng nhập từ khóa tìm kiếm');
        return;
    }
    
    performSearch(query);
}

// Perform search
async function performSearch(query) {
    try {
        // Show loading
        showLoading();
        hideResults();
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                limit: 10
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading
        hideLoading();
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.message || 'Có lỗi xảy ra khi tìm kiếm');
        }
        
    } catch (error) {
        hideLoading();
        showError('Không thể kết nối đến server. Vui lòng thử lại sau.');
        console.error('Search error:', error);
    }
}

// Display search results
function displayResults(data) {
    const { query, results, total_results } = data;
    
    // Update search info
    searchQuery.textContent = query;
    resultsCount.textContent = total_results;
    
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    if (results && results.length > 0) {
        // Show results section
        showResults();
        
        // Create result items
        results.forEach(item => {
            const newsItem = createNewsItem(item);
            resultsContainer.appendChild(newsItem);
        });
        
        // Smooth scroll to results
        resultsSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
        
    } else {
        // Show no results
        showNoResults();
    }
}

// Create news item element
function createNewsItem(item) {
    const newsItem = document.createElement('div');
    newsItem.className = 'news-item';
    
    // Format date
    const date = new Date(item.crawled_at);
    const formattedDate = date.toLocaleDateString('vi-VN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    newsItem.innerHTML = `
        <div class="news-header">
            <div>
                <h3 class="news-title">${escapeHtml(item.title)}</h3>
            </div>
            <div class="news-score">
                ${(item.score * 100).toFixed(1)}%
            </div>
        </div>
        
        <div class="news-content">
            ${escapeHtml(item.content)}
        </div>
        
        <div class="news-meta">
            <div class="news-tags">
                <span class="news-topic">${escapeHtml(item.topic)}</span>
                <span class="news-source">${escapeHtml(item.source)}</span>
            </div>
            <div class="news-date">
                ${formattedDate}
            </div>
        </div>
    `;
    
    // Add click handler to open original article
    newsItem.addEventListener('click', function() {
        if (item.url) {
            window.open(item.url, '_blank');
        }
    });
    
    return newsItem;
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        
        if (response.ok) {
            const data = await response.json();
            
            if (data.success && data.stats) {
                totalDocs.textContent = data.stats.total_documents || '-';
                vocabSize.textContent = data.stats.vocabulary_size || '-';
            }
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Show/Hide functions
function showLoading() {
    loading.classList.add('show');
}

function hideLoading() {
    loading.classList.remove('show');
}

function showResults() {
    resultsSection.classList.add('show');
    noResults.classList.remove('show');
}

function hideResults() {
    resultsSection.classList.remove('show');
    noResults.classList.remove('show');
}

function showNoResults() {
    resultsSection.classList.add('show');
    noResults.classList.add('show');
}

function showError(message) {
    alert(message);
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add some interactive effects
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to suggestion tags
    suggestionTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add focus effect to search input
    searchInput.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    searchInput.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Focus search input when pressing '/' key
    if (e.key === '/' && e.target !== searchInput) {
        e.preventDefault();
        searchInput.focus();
    }
    
    // Clear search when pressing Escape
    if (e.key === 'Escape' && e.target === searchInput) {
        searchInput.value = '';
        hideResults();
    }
});

// Add smooth animations
function addFadeInAnimation(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        element.style.transition = 'all 0.5s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}

