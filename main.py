from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./issues.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class IssueModel(Base):
    __tablename__ = "issues"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="open")
    priority = Column(String, default="low")
    assignee = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic schema
class Issue(BaseModel):
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "open"
    priority: Optional[str] = "low"
    assignee: Optional[str] = ""

class IssueOut(Issue):
    id: str
    createdAt: datetime
    updatedAt: datetime

# FastAPI app
app = FastAPI()

# Allow CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/issues")
def list_issues(
    page: int = 1,
    pageSize: int = 10,
    search: str = "",
    status: str = "",
    priority: str = "",
    assignee: str = "",
    sortColumn: str = "createdAt",
    sortDirection: str = "desc"
):
    session = SessionLocal()
    query = session.query(IssueModel)

    # Filters
    if search:
        query = query.filter(IssueModel.title.contains(search) | IssueModel.description.contains(search))
    if status:
        query = query.filter(IssueModel.status == status)
    if priority:
        query = query.filter(IssueModel.priority == priority)
    if assignee:
        query = query.filter(IssueModel.assignee == assignee)

    # Sorting
    sort_attr = getattr(IssueModel, sortColumn, IssueModel.createdAt)
    if sortDirection == "desc":
        sort_attr = sort_attr.desc()
    query = query.order_by(sort_attr)

    total = query.count()
    issues = query.offset((page-1)*pageSize).limit(pageSize).all()
    session.close()
    return {"total": total, "issues": issues}

@app.get("/issues/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str):
    session = SessionLocal()
    issue = session.query(IssueModel).filter(IssueModel.id == issue_id).first()
    session.close()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@app.post("/issues", response_model=IssueOut)
def create_issue(issue: Issue):
    session = SessionLocal()
    new_issue = IssueModel(
        id=str(uuid4()),
        title=issue.title,
        description=issue.description,
        status=issue.status,
        priority=issue.priority,
        assignee=issue.assignee,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    session.add(new_issue)
    session.commit()
    session.refresh(new_issue)
    session.close()
    return new_issue

@app.put("/issues/{issue_id}", response_model=IssueOut)
def update_issue(issue_id: str, issue: Issue):
    session = SessionLocal()
    db_issue = session.query(IssueModel).filter(IssueModel.id == issue_id).first()
    if not db_issue:
        session.close()
        raise HTTPException(status_code=404, detail="Issue not found")
    db_issue.title = issue.title
    db_issue.description = issue.description
    db_issue.status = issue.status
    db_issue.priority = issue.priority
    db_issue.assignee = issue.assignee
    db_issue.updatedAt = datetime.utcnow()
    session.commit()
    session.refresh(db_issue)
    session.close()
    return db_issue

@app.delete("/issues/{issue_id}")
def delete_issue(issue_id: str):
    session = SessionLocal()
    db_issue = session.query(IssueModel).filter(IssueModel.id == issue_id).first()
    if not db_issue:
        session.close()
        raise HTTPException(status_code=404, detail="Issue not found")
    session.delete(db_issue)
    session.commit()
    session.close()
    return {"detail": "Issue deleted successfully"}
