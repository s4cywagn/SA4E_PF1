// server.js
require("dotenv").config(); // For reading env vars from .env or docker-compose
const express = require("express");
const { Pool } = require("pg");

const app = express();
app.use(express.json());

// Load environment variables
const {
  DATABASE_HOST,
  DATABASE_USER,
  DATABASE_PASSWORD,
  DATABASE_NAME,
  DATABASE_PORT,
  PORT,
} = process.env;

// PostgreSQL connection pool
const pool = new Pool({
  host: DATABASE_HOST || "localhost",
  user: DATABASE_USER || "xmasuser",
  password: DATABASE_PASSWORD || "xmaspassword",
  database: DATABASE_NAME || "xmasdb",
  port: DATABASE_PORT || 5432,
});

// Simple route to check server health
app.get("/", (req, res) => {
  res.send("XmasWishes API is running!");
});

// GET /wishes - retrieve all wishes
app.get("/wishes", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM wishes ORDER BY id ASC");
    res.json(result.rows);
  } catch (err) {
    console.error("Error fetching wishes:", err);
    res.status(500).json({ error: "Failed to fetch wishes" });
  }
});

// POST /wishes - create a new wish
app.post("/wishes", async (req, res) => {
  try {
    const { text } = req.body;
    if (!text) {
      return res.status(400).json({ error: "Missing text in request body" });
    }

    const queryText = "INSERT INTO wishes (text) VALUES ($1) RETURNING *";
    const result = await pool.query(queryText, [text]);

    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error("Error inserting wish:", err);
    res.status(500).json({ error: "Failed to create wish" });
  }
});

// Start the server
const serverPort = PORT || 3000;
app.listen(serverPort, () => {
  console.log(`XmasWishes server is listening on port ${serverPort}`);
});
