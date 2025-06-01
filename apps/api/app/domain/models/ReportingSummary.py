from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class ReportingSummaryBase:
    invoice_name: int
    school_name: str
    class_name: str
    nb_hours: float
    nb_students: int
    teacher_name: str
    billed_at: Optional[datetime] = None
    is_certifying: bool = False
    created_at: Optional[datetime] = datetime.now(timezone.utc)

@dataclass
class ReportingSummaryCreate(ReportingSummaryBase):
    pass


@dataclass
class ReportingSummary(ReportingSummaryBase):
    id: Optional[str] = None

@dataclass
class ReportingSummaryFilter:
    school_name: Optional[str] = None
    class_name: Optional[str] = None
    teacher_name: Optional[str] = None
    invoice_name: Optional[int] = None

    is_certifying: Optional[bool] = None

    min_hours: Optional[float] = None
    max_hours: Optional[float] = None

    min_students: Optional[int] = None
    max_students: Optional[int] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
@dataclass
class CertificationTotals:
    total_hours: float
    total_students: int
    group_count: int

@dataclass
class TotalsByCertification:
    certifying: CertificationTotals
    not_certifying: CertificationTotals
    number_of_teachers : int
    
@dataclass
class ReportingSummaryGrouped:
    school_name: str
    class_name: str
    is_certifying: bool
    total_hours: float
    total_students: int
    summary_count: int
