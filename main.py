from typing import Optional, List
from sqlmodel import SQLModel, Field, Session, create_engine, select
from fastapi import FastAPI, Depends

class Partner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    arr: int = 0
    status: str = "active"
    notes: Optional[str] = None

# In-memory DB for Vercel (resets on restart, perfect for demo)
engine = create_engine("sqlite://", echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI(title="PartnerHub API")

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
