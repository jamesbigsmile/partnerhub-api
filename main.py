from typing import Optional, List
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel, Field as PydanticField

class Partner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    arr: int = 0
    status: str = "active"
    notes: Optional[str] = None

class SQLRequest(BaseModel):
    sql: str = PydanticField(..., example="SELECT * FROM partner WHERE type='ISV'")

app = FastAPI(title="PartnerHub API")

engine = create_engine("sqlite:///:memory:", echo=True)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/partners/", response_model=Partner)
def create_partner(partner: Partner = Body(..., example={
    "name": "AcmeCorp", 
    "type": "ISV", 
    "arr": 400000,
    "status": "active",
    "notes": "Key strategic partner"
}), db: Session = Depends(get_db)):
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

@app.get("/partners/", response_model=List[Partner])
def get_partners(db: Session = Depends(get_db), type_: Optional[str] = "ISV") -> List[Partner]:
    query = select(Partner)
    if type_:
        query = query.where(Partner.type == type_)
    return db.exec(query).all()

@app.post("/sql/execute/")
def execute_sql(request: SQLRequest, db: Session = Depends(get_db)):
    try:
        result = db.exec(request.sql).all()
        return {"sql": request.sql, "results": result}
    except Exception as e:
        return {"error": str(e)}

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
