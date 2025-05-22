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

    def create(self, reporting: ReportingSummaryCreateDTO) -> ReportingSummaryDTO:
        created = self.reporting_service.create_summary(reporting)
        
        return domain_to_dto(created)

    def filtered(self, filters: ReportingSummaryFilterDTO) -> List[ReportingSummaryDTO]:
        reports = self.reporting_service.filtered(filters)
        if not reports:
            return []
        return [domain_to_dto(report) for report in reports]

    def total(self) -> TotalsByCertificationDTO:
        reports = self.reporting_service.get_totals_by_certification()
        if not reports:
            return []
        return to_totals_by_certification(reports)