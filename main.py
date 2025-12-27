from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body
from datetime import datetime

app = FastAPI(title="PartnerHub API 🚀")

class Partner(BaseModel):
    id: int
    name: str
    type: str
    arr: int
    status: str = "active"
    notes: Optional[str] = None

# PRE-SEED DEMO DATA (Vercel-proof)
DEMO_PARTNERS = [
    Partner(id=1, name="CloudCo", type="ISV", arr=250000, notes="Key ARR driver"),
    Partner(id=2, name="TechCorp", type="SI", arr=150000, notes="Implementation partner"),
    Partner(id=3, name="DataCorp", type="ISV", arr=300000),
    Partner(id=4, name="SysInt", type="SI", arr=180000, status="pending"),
]

@app.get("/")
def root():
    return {"message": "PartnerHub API Live!", "docs": "/docs"}

@app.get("/partners/", response_model=List[Partner])
def get_partners(type_: Optional[str] = None, status: Optional[str] = None):
    partners = DEMO_PARTNERS
    if type_:
        partners = [p for p in partners if p.type == type_]
    if status:
        partners = [p for p in partners if p.status == status]
    return partners

@app.get("/partners/{partner_id}", response_model=Partner)
def get_partner(partner_id: int):
    partner = next((p for p in DEMO_PARTNERS if p.id == partner_id), None)
    if not partner:
        return {"error": "Partner not found"}
    return partner

@app.get("/analytics/")
def analytics():
    total_arr = sum(p.arr for p in DEMO_PARTNERS)
    isv_arr = sum(p.arr for p in DEMO_PARTNERS if p.type == "ISV")
    active_count = len([p for p in DEMO_PARTNERS if p.status == "active"])
    return {
        "total_arr": total_arr,
        "isv_arr": isv_arr,
        "active_partners": active_count,
        "sql_equivalent": "SELECT SUM(arr), COUNT(*) FROM partner WHERE status='active'"
    }

@app.get("/sql-examples/")
def sql_examples():
    return {
        "queries": [
            "SELECT type, SUM(arr) FROM partner GROUP BY type",
            "SELECT COUNT(*) FROM partner WHERE status='active'", 
            "SELECT name, arr FROM partner ORDER BY arr DESC LIMIT 3"
        ]
    }
