from typing import Optional, List
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI, Depends
from pydantic import BaseModel

class Partner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    arr: int = 0
    status: str = "active"
    notes: Optional[str] = None

app = FastAPI(title="PartnerHub API")

# Vercel serverless SQLite (ephemeral)
engine = create_engine("sqlite:///:memory:", echo=True)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/partners/")
def create_partner(partner: Partner, db: Session = Depends(get_db)):
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

@app.get("/partners/")
def get_partners(db: Session = Depends(get_db), type_: Optional[str] = None) -> List[Partner]:
    query = select(Partner)
    if type_:
        query = query.where(Partner.type == type_)
    return db.exec(query).all()

@app.get("/seed/")
def seed_data(db: Session = Depends(get_db)):
    demo_partners = [
        Partner(name="CloudCo", type="ISV", arr=250000),
        Partner(name="TechCorp", type="SI", arr=150000)
    ]
    for p in demo_partners:
        db.add(p)
    db.commit()
    return {"message": "Seeded demo data"}
