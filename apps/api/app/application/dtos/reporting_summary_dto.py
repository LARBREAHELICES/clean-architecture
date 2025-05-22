from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# Base commune
class ReportingSummaryBaseDTO(BaseModel):
    invoice_name: int
    school_name: Optional[str]
    class_name: Optional[str]
    nb_hours: Optional[float]
    nb_students: Optional[int]
    teacher_name: Optional[str]
    billed_at: Optional[datetime]
    is_certifying: bool = True
    model_config = {
        "from_attributes": True
    }


# Pour la création (POST) — sans id ni created_at
class ReportingSummaryCreateDTO(ReportingSummaryBaseDTO):
    pass

# Pour la mise à jour (PUT / PATCH)
class ReportingSummaryUpdateDTO(BaseModel):
    invoice_name: Optional[int] = None
    school_name: Optional[str] = None
    class_name: Optional[str] = None
    nb_hours: Optional[float] = None
    nb_students: Optional[int] = None
    teacher_name: Optional[str] = None
    billed_at: Optional[datetime] = None
    is_certifying: bool = True

    model_config = {
        "from_attributes": True
    }

class ReportingSummaryGroupedDTO(BaseModel):
    school_name: str
    class_name: str
    is_certifying: bool
    total_hours: float
    total_students: int
    summary_count: int

# Pour la lecture (GET)
class ReportingSummaryDTO(ReportingSummaryBaseDTO):
    id: UUID
    created_at: datetime

# Pour les filtres 
class ReportingSummaryFilterDTO(BaseModel):
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
    
class CertificationTotalsDTO(BaseModel):
    total_hours: float
    total_students: int
    group_count: int

class TotalsByCertificationDTO(BaseModel):
    certifying: CertificationTotalsDTO
    not_certifying: CertificationTotalsDTO
    
class ReportingSummaryGroupedDTO(BaseModel):
    school_name: str
    class_name: str
    is_certifying: bool
    total_hours: float
    total_students: int
    summary_count: int