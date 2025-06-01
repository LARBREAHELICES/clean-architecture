from typing import Optional
from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime

#  Mixin pour nettoyage des chaînes
class CleanStrMixin:
    @classmethod
    def _clean_string(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return " ".join(value.strip().split())


# Base commune
class ReportingSummaryBaseDTO(BaseModel, CleanStrMixin):
    invoice_name: int
    school_name: Optional[str]
    class_name: Optional[str]
    nb_hours: Optional[float]
    nb_students: Optional[int]
    teacher_name: Optional[str]
    billed_at: Optional[datetime]
    is_certifying: Optional[bool]

    model_config = {
        "from_attributes": True
    }

    @field_validator("school_name", "class_name", "teacher_name", mode="before")
    @classmethod
    def clean_strings(cls, value):
        return cls._clean_string(value)


# Pour la création (POST) — sans id ni created_at
class ReportingSummaryCreateDTO(ReportingSummaryBaseDTO):
    pass


# Pour la mise à jour (PUT / PATCH)
class ReportingSummaryUpdateDTO(BaseModel, CleanStrMixin):
    invoice_name: Optional[int] = None
    school_name: Optional[str] = None
    class_name: Optional[str] = None
    nb_hours: Optional[float] = None
    nb_students: Optional[int] = None
    teacher_name: Optional[str] = None
    billed_at: Optional[datetime] = None
    is_certifying: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }

    @field_validator("school_name", "class_name", "teacher_name", mode="before")
    @classmethod
    def clean_strings(cls, value):
        return cls._clean_string(value)


class ReportingSummaryGroupedDTO(BaseModel):
    school_name: str
    class_name: str
    is_certifying: bool
    total_hours: float
    total_students: int
    summary_count: int


# Pour la lecture (GET)
class ReportingSummaryDTO(ReportingSummaryGroupedDTO):
    id: UUID
    created_at: datetime


# Pour les filtres 
class ReportingSummaryFilterDTO(BaseModel, CleanStrMixin):
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

    @field_validator("school_name", "class_name", "teacher_name", mode="before")
    @classmethod
    def clean_strings(cls, value):
        return cls._clean_string(value)


class CertificationTotalsDTO(BaseModel):
    total_hours: float
    total_students: int
    group_count: int


class TotalsByCertificationDTO(BaseModel):
    certifying: CertificationTotalsDTO
    not_certifying: CertificationTotalsDTO
    number_of_teachers: int
