# app/infrastructure/db/models/reporting_summary_db.py

import uuid
from uuid import UUID
from typing import Optional
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field

class ReportingSummaryBase(SQLModel):
    invoice_name: int
    school_name: str
    class_name: str
    nb_hours: float
    nb_students: int
    teacher_name: str
    billed_at: datetime
    is_certifying: bool

class ReportingSummaryCreateDB(ReportingSummaryBase):
    pass

class ReportingSummaryDB(ReportingSummaryBase, table=True):
    __tablename__ = "reporting_summary"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
