from app.application.dtos.reporting_summary_dto import (
    ReportingSummaryDTO,
    ReportingSummaryGroupedDTO, 
    ReportingSummaryFilterDTO,
    CertificationTotalsDTO,
    TotalsByCertificationDTO
)
from app.domain.models.ReportingSummary import ( 
    ReportingSummary, ReportingSummaryFilter
)# à adapter selon ton modèle domaine

from typing import List, Tuple
from sqlalchemy.engine import Row

def dto_to_domain(dto: ReportingSummaryDTO) -> ReportingSummary:
    """Convertit un DTO de création en modèle domaine"""
    return ReportingSummary(
        invoice_name=dto.invoice_name,
        school_name=dto.school_name,
        class_name=dto.class_name,
        nb_hours=dto.nb_hours,
        nb_students=dto.nb_students,
        teacher_name=dto.teacher_name,
        billed_at=dto.billed_at,
        created_at=dto.created_at,
        is_certifying=dto.is_certifying,
    )

def domain_to_dto(domain: ReportingSummary) -> ReportingSummaryDTO:
    """Convertit un modèle domaine en DTO de lecture"""
    return ReportingSummaryDTO(
        id=domain.id,
        invoice_name=domain.invoice_name,
        school_name=domain.school_name,
        class_name=domain.class_name,
        nb_hours=domain.nb_hours,
        nb_students=domain.nb_students,
        teacher_name=domain.teacher_name,
        billed_at=domain.billed_at,
        created_at=domain.created_at,
        is_certifying=domain.is_certifying,
    )

def to_grouped_dto_list(rows: List[Row]) -> List[ReportingSummaryGroupedDTO]:
    return [
        ReportingSummaryGroupedDTO(
            school_name=row.school_name,
            class_name=row.class_name,
            is_certifying=row.is_certifying,
            total_hours=row.total_hours,
            total_students=row.total_students,
            summary_count=row.summary_count,
        )
        for row in rows
    ]

def to_domain_filter(dto: ReportingSummaryFilterDTO) -> ReportingSummaryFilter:
    return ReportingSummaryFilter(
        school_name=dto.school_name,
        class_name=dto.class_name,
        teacher_name=dto.teacher_name,
        invoice_name=dto.invoice_name,
        is_certifying=dto.is_certifying,
        min_hours=dto.min_hours,
        max_hours=dto.max_hours,
        min_students=dto.min_students,
        max_students=dto.max_students,
        start_date=dto.start_date,
        end_date=dto.end_date,
    )

def to_totals_by_certification(rows) -> TotalsByCertificationDTO:

    certifying = CertificationTotalsDTO(
        total_hours=rows.certifying.total_hours,
        total_students=rows.certifying.total_students,
        group_count=rows.certifying.group_count
    )

    not_certifying = CertificationTotalsDTO(
        total_hours=rows.not_certifying.total_hours,
        total_students=rows.not_certifying.total_students,
        group_count=rows.not_certifying.group_count
    )

    return TotalsByCertificationDTO(
        certifying=certifying,
        not_certifying=not_certifying,
        number_of_teachers=rows.number_of_teachers
    )