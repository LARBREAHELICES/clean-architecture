from datetime import datetime

from app.domain.interfaces.ReportingSummaryProtocol import ReportingSummaryProtocol

from app.domain.models.ReportingSummary import (
    ReportingSummary, 
    ReportingSummaryFilter,
    TotalsByCertification
)

class ReportingSummaryService:
    def __init__(self, repository: ReportingSummaryProtocol):
        self.repository = repository

    def create_summary(self, reporting: ReportingSummary) -> ReportingSummary | None:
        """
        Create a new reporting summary.
        """
        return self.repository.create_summary(reporting)
    
    def list_all_summaries(self) -> list[ReportingSummary] | None:
        """
        List all reporting summaries.
        """
        return self.repository.list_all_summaries()
    
    def get_grouped_summary(self)->list[ReportingSummary] | None:
        
        return self.repository.get_grouped_summary()
    
    def filtered(self, filters : ReportingSummaryFilter) -> list[ReportingSummary] | None:
        
        return self.repository.get_filtered_summaries(filters)
    
    def get_totals_by_certification(self) -> TotalsByCertification | None:
        """
        Get the total number of students and hours by certification.
        """
        return self.repository.get_totals_by_certification()
   
    def get_last_invoice_name(self) -> str | None:
        """
        Get the last invoice date.
        """
        return self.repository.get_last_invoice_name()