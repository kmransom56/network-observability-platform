# NeDi Integration Guide

This guide explains how to integrate the AI Assistant with your existing NeDi web interface at `nedi.netintegrate.net`.


## Integration Options

### Option 1: Embed AI Assistant in NeDi Pages

Add AI Assistant functionality directly to NeDi PHP pages:

```php
<!-- In Devices-Status.php or similar -->
<div id="ai-assistant-widget">
    <iframe 
        src="http://localhost:11047/app/static/ai_assistant.html" 
        width="100%" 
        height="600px"
        style="border: none;">
    </iframe>
</div>
```

### Option 2: Add AI Assistant Link/Button

Add a button that opens AI Assistant in a new window:

```php
<!-- In NeDi navigation or device status page -->
<a href="http://localhost:11047/app/static/ai_assistant.html" 
   target="_blank"
   class="ai-assistant-btn">
    🤖 AI Assistant
</a>
```

### Option 3: AJAX Integration

Call AI Assistant API directly from NeDi pages:

```javascript
// In NeDi JavaScript
async function auditDeviceConfig(deviceIp) {
    const response = await fetch('http://localhost:11047/api/ai/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            target: `/var/nedi/data/fortigate_api/${deviceIp}_*.json`,
            audit_type: 'config'
        })
    });
    const result = await response.json();
    // Display results in NeDi interface
    displayAuditResults(result.findings);
}
```

## Configuration

### 1. CORS Setup

Ensure FastAPI allows requests from NeDi domain:

```python
# In app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nedi.netintegrate.net",
        "http://localhost:11047",
        "*"  # For development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Backend URL Configuration

If running AI Assistant on different server:

```bash
# Environment variable
export AI_ASSISTANT_URL="http://your-server:11047"

# Or in NeDi config
# Add to nedi.conf or PHP config
define('AI_ASSISTANT_URL', 'http://your-server:11047');
```

### 3. Reverse Proxy Setup

If you want AI Assistant accessible via same domain:

```nginx
# nginx configuration
location /ai-assistant/ {
    proxy_pass http://localhost:11047/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Then access via: `https://nedi.netintegrate.net/ai-assistant/app/static/ai_assistant.html`

## Use Cases

### 1. Device Configuration Audit

```javascript
// Audit FortiGate configuration
function auditFortiGate(deviceIp) {
    fetch('http://localhost:11047/api/ai/audit', {
        method: 'POST',
        body: JSON.stringify({
            target: `/var/nedi/data/fortigate_api/${deviceIp}_*.json`,
            audit_type: 'security'
        })
    })
    .then(r => r.json())
    .then(data => {
        // Show audit results in NeDi interface
        showNotification('Security Audit', data.findings);
    });
}
```

### 2. Network Issue Repair

```javascript
// Get AI suggestions for network issues
function getRepairSuggestions(issue, deviceIp) {
    fetch('http://localhost:11047/api/ai/repair', {
        method: 'POST',
        body: JSON.stringify({
            issue: issue,
            file_path: `/var/nedi/inc/libfortigate.pm`
        })
    })
    .then(r => r.json())
    .then(data => {
        // Display repair suggestions
        showRepairDialog(data.fix);
    });
}
```

### 3. Learn from Network Topology

```javascript
// Learn from network topology data
function learnTopology() {
    fetch('http://localhost:11047/api/ai/learn', {
        method: 'POST',
        body: JSON.stringify({
            source: '/var/nedi/data/',
            topic: 'network topology'
        })
    })
    .then(r => r.json())
    .then(data => {
        // Use knowledge for recommendations
        applyNetworkRecommendations(data.knowledge);
    });
}
```

## Security Considerations

1. **HTTPS**: Use HTTPS for production (your NeDi is already on HTTPS)
2. **Authentication**: Add API key or session-based auth
3. **Rate Limiting**: Prevent abuse of AI endpoints
4. **Input Validation**: Validate all inputs from NeDi interface

## Example: Adding AI Button to NeDi

```php
<!-- Add to NeDi template or header -->
<div class="ai-assistant-container">
    <button onclick="openAIAssistant()" class="btn btn-primary">
        🤖 AI Assistant
    </button>
</div>

<script>
function openAIAssistant() {
    // Open in modal or new window
    window.open(
        'http://localhost:11047/app/static/ai_assistant.html',
        'AIAssistant',
        'width=1200,height=800'
    );
}

// Or embed directly
function embedAIAssistant() {
    const container = document.getElementById('ai-assistant-widget');
    container.innerHTML = `
        <iframe 
            src="http://localhost:11047/app/static/ai_assistant.html"
            width="100%"
            height="600px"
            style="border: 1px solid #ccc; border-radius: 4px;">
        </iframe>
    `;
}
</script>
```

## Troubleshooting

### Connection Issues

If "Connecting..." persists:

1. **Check FastAPI is running:**
   ```bash
   ./scripts/start_api.sh
   ```

2. **Verify port is accessible:**
   ```bash
   curl http://localhost:11047/health
   ```

3. **Check CORS settings** in `app/main.py`

4. **Verify backend URL** in JavaScript:
   ```javascript
   const API_BASE = '/api/ai';  // Relative (same domain)
   // OR
   const API_BASE = 'http://localhost:11047/api/ai';  // Absolute
   ```

### Mixed Content (HTTP/HTTPS)

If NeDi is HTTPS but AI Assistant is HTTP:

- Use HTTPS for AI Assistant (recommended)
- Or use reverse proxy to serve both on same domain
- Or allow mixed content (not recommended for production)

## Next Steps

1. **Start AI Assistant server:**
   ```bash
   cd ~/network-observability-platform
   ./scripts/start_api.sh
   ```

2. **Test connection:**
   ```bash
   curl http://localhost:11047/api/ai/status
   ```

3. **Add integration code** to NeDi PHP pages

4. **Configure CORS** for your NeDi domain

5. **Test from NeDi interface**
