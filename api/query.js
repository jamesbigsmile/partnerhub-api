import Database from 'better-sqlite3';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'POST only' });
  }
  
  const { query } = req.body;
  
  try {
    let db = new Database('partners.db');
    
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
    
    // Seed initial data
    db.exec(`
      INSERT OR IGNORE INTO partners (id, name, type, arr, region, status) VALUES
      (1, 'PartnerForge', 'ISV', 125000, 'NA', 'Active'),
      (2, 'CloudScale', 'ISV', 95000, 'EU', 'Active'),
      (3, 'DataSync Pro', 'ISV', 80000, 'NA', 'Active'),
      (4, 'ProServices', 'Service', 88000, 'NA', 'Active')
    `);
    
    const result = db.prepare(query).all();
    db.close();
    
    res.json({ success: true, rows: result });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
}

