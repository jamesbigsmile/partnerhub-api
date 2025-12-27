import Database from 'better-sqlite3';

const db = new Database('partners.db');

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  
  const { query } = req.body;
  
  try {
    const result = db.exec(query);
    const rows = db.prepare(query).all();
    res.json({ success: true, rows });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
}
