// Dashboard JavaScript functionality

// Generate post preview
function generatePreview() {
    const modal = new bootstrap.Modal(document.getElementById('previewModal'));
    const loadingDiv = document.getElementById('previewLoading');
    const contentDiv = document.getElementById('previewContent');
    const errorDiv = document.getElementById('previewError');
    
    // Reset modal state
    loadingDiv.style.display = 'block';
    contentDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    
    modal.show();
    
    // Make request to generate preview
    fetch('/generate_preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        loadingDiv.style.display = 'none';
        
        if (data.error) {
            document.getElementById('errorMessage').textContent = data.error;
            errorDiv.style.display = 'block';
        } else {
            document.getElementById('postContent').value = data.content;
            contentDiv.style.display = 'block';
        }
    })
    .catch(error => {
        loadingDiv.style.display = 'none';
        document.getElementById('errorMessage').textContent = 'Network error: ' + error.message;
        errorDiv.style.display = 'block';
    });
}

// Test connections
function testConnections() {
    const modal = new bootstrap.Modal(document.getElementById('connectionModal'));
    const loadingDiv = document.getElementById('connectionLoading');
    const resultsDiv = document.getElementById('connectionResults');
    
    // Reset modal state
    loadingDiv.style.display = 'block';
    resultsDiv.style.display = 'none';
    
    modal.show();
    
    // Make request to test connections
    fetch('/test_connections')
    .then(response => response.json())
    .then(data => {
        loadingDiv.style.display = 'none';
        
        if (data.error) {
            resultsDiv.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${data.error}
                </div>
            `;
        } else {
            let resultsHtml = '<div class="row">';
            
            // Telegram results
            if (data.telegram) {
                const status = data.telegram.status;
                const alertClass = status === 'success' ? 'success' : 'danger';
                const icon = status === 'success' ? 'check-circle' : 'exclamation-triangle';
                
                resultsHtml += `
                    <div class="col-md-6 mb-3">
                        <div class="alert alert-${alertClass}" role="alert">
                            <h6 class="mb-2">
                                <i class="fab fa-telegram me-2"></i>Telegram Bot
                                <i class="fas fa-${icon} float-end"></i>
                            </h6>
                `;
                
                if (status === 'success') {
                    resultsHtml += `
                        <p class="mb-1"><strong>Bot Name:</strong> ${data.telegram.bot_name}</p>
                        <p class="mb-0"><strong>Username:</strong> @${data.telegram.username}</p>
                    `;
                } else {
                    resultsHtml += `<p class="mb-0">${data.telegram.message}</p>`;
                }
                
                resultsHtml += '</div></div>';
            }
            
            // OpenAI results
            if (data.openai) {
                const status = data.openai.status;
                const alertClass = status === 'success' ? 'success' : 'danger';
                const icon = status === 'success' ? 'check-circle' : 'exclamation-triangle';
                
                resultsHtml += `
                    <div class="col-md-6 mb-3">
                        <div class="alert alert-${alertClass}" role="alert">
                            <h6 class="mb-2">
                                <i class="fas fa-brain me-2"></i>OpenAI API
                                <i class="fas fa-${icon} float-end"></i>
                            </h6>
                `;
                
                if (status === 'success') {
                    resultsHtml += `<p class="mb-0"><strong>Model:</strong> ${data.openai.model}</p>`;
                } else {
                    resultsHtml += `<p class="mb-0">${data.openai.message}</p>`;
                }
                
                resultsHtml += '</div></div>';
            }
            
            resultsHtml += '</div>';
            resultsDiv.innerHTML = resultsHtml;
        }
        
        resultsDiv.style.display = 'block';
    })
    .catch(error => {
        loadingDiv.style.display = 'none';
        resultsDiv.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Network error: ${error.message}
            </div>
        `;
        resultsDiv.style.display = 'block';
    });
}

// Auto-refresh dashboard every 30 seconds if scheduler is running
document.addEventListener('DOMContentLoaded', function() {
    const schedulerBadge = document.querySelector('.badge.bg-success');
    if (schedulerBadge && schedulerBadge.textContent.includes('Active')) {
        setInterval(function() {
            // Only refresh if still on dashboard page
            if (window.location.pathname === '/') {
                location.reload();
            }
        }, 30000); // 30 seconds
    }
});

// Form validation helpers
function validateConfigForm() {
    const botToken = document.getElementById('bot_token');
    const channelId = document.getElementById('channel_id');
    const openaiKey = document.getElementById('openai_api_key');
    
    if (botToken && botToken.value && !botToken.value.includes(':')) {
        alert('Bot token should contain a colon (:) - format: 123456789:AABBCCDDEEFFgghhiijjkkllmmnnooppqq');
        return false;
    }
    
    if (channelId && channelId.value && !channelId.value.startsWith('@') && !channelId.value.startsWith('-')) {
        alert('Channel ID should start with @ (username) or - (numeric ID)');
        return false;
    }
    
    if (openaiKey && openaiKey.value && !openaiKey.value.startsWith('sk-')) {
        alert('OpenAI API key should start with "sk-"');
        return false;
    }
    
    return true;
}

// Add form validation to config form if it exists
document.addEventListener('DOMContentLoaded', function() {
    const configForm = document.querySelector('form[method="POST"]');
    if (configForm && window.location.pathname.includes('/config')) {
        configForm.addEventListener('submit', function(e) {
            if (!validateConfigForm()) {
                e.preventDefault();
            }
        });
    }
});
