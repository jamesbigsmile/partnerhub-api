const Database = require('better-sqlite3');
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const db = new Database('data/partners.db');

// Auto-create table + seed data
db.exec(`
  CREATE TABLE IF NOT EXISTS partners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    arr INTEGER,
    region TEXT,
    status TEXT DEFAULT 'Active'
  )
`);

db.exec(`
  INSERT OR IGNORE INTO partners (id, name, type, arr, region, status) VALUES
  (1, 'PartnerForge', 'ISV', 125000, 'NA', 'Active'),
  (2, 'CloudScale', 'ISV', 95000, 'EU', 'Active'),
  (3, 'DataSync Pro', 'ISV', 80000, 'NA', 'Active'),
  (4, 'ProServices', 'Service', 88000, 'NA', 'Active')
`);

app.post('/api/query', (req, res) => {
  try {
    const { query } = req.body;
    const result = db.prepare(query).all();
    res.json({ success: true, rows: result });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/api/partners', (req, res) => {
  const result = db.prepare('SELECT * FROM partners').all();
  res.json({ success: true, rows: result });
});

app.listen(3001, () => {
  console.log('🗄️ Local DB Server: http://localhost:3001');
  console.log('📊 Test data: http://localhost:3001/api/partners');
});
