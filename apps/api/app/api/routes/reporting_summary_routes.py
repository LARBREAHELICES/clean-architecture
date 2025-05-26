from fastapi import APIRouter, Depends
from typing import List

from app.application.dtos.reporting_summary_dto import (
    ReportingSummaryDTO,
    ReportingSummaryCreateDTO, 
    ReportingSummaryGroupedDTO,
    ReportingSummaryFilterDTO,
    TotalsByCertificationDTO
)
from app.application.controllers.reporting_summary_controller import ReportingSummaryController
from app.api.deps import get_reporting_summary_controller

router = APIRouter()

# Lister tous les rapports
@router.get("/all", response_model=List[ReportingSummaryDTO])
def list_reporting_summaries(
    controller: ReportingSummaryController = Depends(get_reporting_summary_controller),
):
    return controller.get_all()

@router.get("/regrouped", response_model=List[ReportingSummaryGroupedDTO])
def list_reporting_summaries(
    controller: ReportingSummaryController = Depends(get_reporting_summary_controller),
):
    return controller.regrouped()

# Créer un rapport
@router.post("/", response_model=ReportingSummaryDTO)
def create_reporting_summary(
    data: ReportingSummaryCreateDTO,
    controller: ReportingSummaryController = Depends(get_reporting_summary_controller),
):
    return controller.create(data)

# filtre
@router.post("/filter", response_model=List[ReportingSummaryDTO])
def filter_reporting_summaries(
    filters: ReportingSummaryFilterDTO,
    controller: ReportingSummaryController = Depends(get_reporting_summary_controller),
):
    return controller.filtered(filters)

@router.get("/totals-by-certification", response_model=TotalsByCertificationDTO)
def get_totals_by_certification(
    controller : ReportingSummaryController = Depends(get_reporting_summary_controller)
    ):
    
    return controller.total()

@router.get("/last-invoice-name", response_model=int)
def get_last_invoice_name(
    controller : ReportingSummaryController = Depends(get_reporting_summary_controller)
    ):
    
    return controller.get_last_invoice_name()