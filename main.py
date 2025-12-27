from typing import Optional, List
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI, Depends, Body
import sqlalchemy

app = FastAPI(title="PartnerHub API")

class Partner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    arr: int = 0
    status: str = "active"
    notes: Optional[str] = None

# FIXED: Vercel serverless SQLite
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False},
    poolclass=sqlalchemy.pool.StaticPool
)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "PartnerHub API Live!", "docs": "/docs"}

@app.post("/partners/")
def create_partner(partner: Partner = Body(...), db: Session = Depends(get_db)):
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

@app.get("/partners/", response_model=List[Partner])
def get_partners(db: Session = Depends(get_db), type_: Optional[str] = None):
    query = select(Partner)
    if type_:
        query = query.where(Partner.type == type_)
    return db.exec(query).all()

@app.get("/seed/")
def seed_data(db: Session = Depends(get_db)):
    partners = [
        Partner(name="CloudCo", type="ISV", arr=250000),
        Partner(name="TechCorp", type="SI", arr=150000)
    ]
    for p in partners:
        db.add(p)
    db.commit()
    return {"seeded": 2}
