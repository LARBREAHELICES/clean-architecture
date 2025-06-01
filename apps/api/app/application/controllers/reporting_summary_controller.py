from typing import List

from app.domain.services.reporting_service import ReportingSummaryService
from app.application.dtos.reporting_summary_dto import (
    ReportingSummaryDTO,ReportingSummaryCreateDTO, ReportingSummaryFilterDTO, TotalsByCertificationDTO,
    ReportingSummaryGroupedDTO
)

from app.application.mappers.reporting_summary_mapper import (
    domain_to_dto, to_grouped_dto_list, to_totals_by_certification)

class ReportingSummaryController:
    def __init__(self, reporting_service: ReportingSummaryService):
        self.reporting_service = reporting_service

    def get_all(self) -> List[ReportingSummaryDTO]:
        reports = self.reporting_service.list_all_summaries()
        if not reports:
            return []
        return [domain_to_dto(report) for report in reports]
    
    def regrouped(self) -> List[ReportingSummaryGroupedDTO]:
        reports = self.reporting_service.get_grouped_summary()
        if not reports:
            return []
        
        return to_grouped_dto_list(reports)

    def create(self, reporting: ReportingSummaryCreateDTO) -> ReportingSummaryDTO | None:
        created = self.reporting_service.create_summary(reporting)
        
        if not created:
            return None
        # Convert the created domain object to DTO
        
        return domain_to_dto(created)

    def filtered(self, filters: ReportingSummaryFilterDTO) -> List[ReportingSummaryDTO]:
        reports = self.reporting_service.filtered(filters)
        if not reports:
            return []
        return [domain_to_dto(report) for report in reports]

    def total(self) -> TotalsByCertificationDTO | None:
        reports = self.reporting_service.get_totals_by_certification()
        if not reports:
            return None
        return to_totals_by_certification(reports)
    
    def get_last_invoice_name(self) -> str:
        last_invoice_name = self.reporting_service.get_last_invoice_name()
        if not last_invoice_name:
            return ""
        return last_invoice_name