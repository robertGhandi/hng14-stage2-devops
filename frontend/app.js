const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

// ✅ FIX: use environment variable instead of hardcoded localhost
const API_URL = process.env.API_URL || "http://api:8000";

app.use(express.json());

// safer static path handling
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    console.error("Submit job error:", err.message);
    res.status(500).json({ error: "Failed to submit job" });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    console.error("Status fetch error:", err.message);
    res.status(500).json({ error: "Failed to fetch job status" });
  }
});

app.listen(3000, () => {
  console.log('Frontend running on port 3000');
});