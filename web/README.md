# Legends of Minds - Web Dashboard

## Overview

A terminal-style web dashboard providing real-time monitoring and interaction with the Legends of Minds AI system.

## Features

### 🛡️ Safety Verification Dashboard
- One-click full safety verification
- Individual safety check execution
- Real-time status reporting
- Clear pass/fail indicators

### 📊 System Monitoring
- Service health checks
- Resource usage monitoring (CPU, RAM, GPU)
- Network isolation verification
- Process isolation checks

### 🤖 Model Interaction
- Select and test available models
- Generate text from prompts
- View model responses
- Model list refresh

### 📁 File Management
- Upload files to the knowledge base
- List uploaded documents
- View file metadata
- Collection organization

## Files

- `index.html` - Single-page application with:
  - Terminal-style UI (green on black)
  - Real-time API integration
  - Interactive safety dashboard
  - Model testing interface
  - File upload interface

## Design

### Visual Style
- Retro terminal aesthetic
- Matrix-style green on black
- Monospace font (Courier New)
- Glowing text effects
- Responsive grid layout

### Color Coding
- **Green (#0f0)** - Verified, safe, operational
- **Yellow (#ff0)** - Warnings, degraded
- **Red (#f00)** - Errors, failures
- **Cyan (#0ff)** - Information, headers

## Usage

### Accessing the Dashboard

```bash
# Open in your browser
http://localhost:8080
```

The dashboard automatically connects to:
- Control Center API: http://localhost:8080
- File Ingest API: http://localhost:8001

### Safety Verification

1. Click "Run Full Safety Verification"
2. Wait for all checks to complete (~30 seconds)
3. Review pass/fail status for each check
4. Investigate any warnings

### Model Testing

1. Select a model from dropdown (or refresh list)
2. Enter a prompt in the text area
3. Click "Generate"
4. View response in output box

### File Upload

1. Click "Choose File" and select a document
2. Click "Upload File"
3. View upload confirmation
4. Click "List Uploaded Files" to see all files

## API Integration

The dashboard uses fetch API to communicate with:

### Control Center Endpoints
```javascript
GET  /health                     - System health
GET  /api/models                 - List models
POST /api/generate               - Generate text
GET  /api/safety/full_report     - Full safety report
GET  /api/safety/*               - Individual checks
```

### Ingest Service Endpoints
```javascript
GET  /health                     - Service health
GET  /api/files                  - List files
POST /api/upload                 - Upload file
```

## Customization

### Changing Colors

Edit the CSS in `<style>` section:
```css
body {
    background: #000;  /* Background color */
    color: #0f0;       /* Default text color */
}

.verified { color: #0f0; }  /* Success color */
.warning { color: #ff0; }   /* Warning color */
.error { color: #f00; }     /* Error color */
```

### Adding New Sections

1. Add HTML section in the dashboard
2. Create corresponding JavaScript function
3. Call API endpoint using fetch
4. Update DOM with results

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

All modern browsers with ES6+ support.

## No Build Required

This is a static HTML file with vanilla JavaScript:
- No npm dependencies
- No build process
- No bundler required
- Just open in a browser

## Security

- All API calls are to localhost
- No external resources loaded
- No CDN dependencies
- No third-party scripts
- Pure HTML/CSS/JS

## Extending

To add new features:

1. Add new button/section in HTML
2. Create JavaScript function
3. Use fetch to call API endpoint
4. Update dashboard with response

Example:
```javascript
async function myNewCheck() {
    try {
        const resp = await fetch('http://localhost:8080/api/my-endpoint');
        const data = await resp.json();
        document.getElementById('output').innerHTML = JSON.stringify(data, null, 2);
    } catch (err) {
        console.error(err);
    }
}
```
