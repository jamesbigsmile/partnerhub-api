# PartnerHub API

FastAPI + SQLModel + SQLite demo tracking SaaS partnerships.

## Live Demo
```
POST /partners/ {"name": "CloudCo", "type": "ISV", "arr": 250000}
GET /partners/
```

## SQL Queries
```sql
SELECT SUM(arr) FROM partner WHERE type='ISV';
```
