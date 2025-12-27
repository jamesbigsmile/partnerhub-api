from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SQLQuery(BaseModel):
    query: str

# Create DB table
conn = sqlite3.connect('partners.db', check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS partners 
                (id INTEGER PRIMARY KEY, name TEXT, type TEXT, arr REAL)''')
# Add demo data
conn.execute("INSERT OR IGNORE INTO partners VALUES (1,'HubSpot','ISV',250000)")
conn.execute("INSERT OR IGNORE INTO partners VALUES (2,'Salesforce','SI',500000)")
conn.execute("INSERT OR IGNORE INTO partners VALUES (3,'Marketo','Referral',75000)")
conn.commit()
conn.close()

@app.post("/execute-sql")
async def execute_sql(query: SQLQuery):
    try:
        conn = sqlite3.connect('partners.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(query.query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()
        return {"success": True, "columns": columns, "rows": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "PartnerHub API - Local SQLite", "status": "ready"}
