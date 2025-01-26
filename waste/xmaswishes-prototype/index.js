const express = require("express");
const app = express();
const bodyParser = require("body-parser");

app.use(bodyParser.json());

// Dummy-Datenhaltung (In-Memory) oder echte DB
let wishes = {};
let currentId = 1;

app.post("/wishes", (req, res) => {
  const wish = {
    id: currentId++,
    text: req.body.text || "Kein Text",
    status: "neu",
    createdAt: new Date(),
  };
  wishes[wish.id] = wish;
  return res.status(201).json(wish);
});

app.get("/wishes/:id", (req, res) => {
  const wish = wishes[req.params.id];
  if (!wish) {
    return res.status(404).json({ error: "Not found" });
  }
  return res.json(wish);
});

app.patch("/wishes/:id", (req, res) => {
  const wish = wishes[req.params.id];
  if (!wish) {
    return res.status(404).json({ error: "Not found" });
  }
  if (req.body.status) wish.status = req.body.status;
  return res.json(wish);
});

app.listen(3000, () => {
  console.log("XmasWishes prototype running on port 3000");
});
