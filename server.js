const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files from the frontend public directory
app.use(express.static(path.join(__dirname, 'frontend', 'public')));

// Serve index.html for all routes (SPA routing)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'public', 'index.html'));
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Frontend server running at http://0.0.0.0:${port}`);
});