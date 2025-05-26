from sqlmodel import Session, select, func
from typing import Protocol, List
from fastapi import Depends
from typing import List

from app.domain.models.ReportingSummary import ReportingSummary, ReportingSummaryBase, ReportingSummaryGrouped
from app.domain.interfaces.ReportingSummaryProtocol import ReportingSummaryProtocol

from app.infrastructure.db.models.ReportingSummaryDB import ReportingSummaryDB

from app.application.dtos.reporting_summary_dto import ( 
    ReportingSummaryDTO, ReportingSummaryFilterDTO, 
    TotalsByCertificationDTO,
    CertificationTotalsDTO
)

class ReportingSummaryRepositoryImpl(ReportingSummaryProtocol):
    def __init__(self, session: Session ):
        self.session = session
        
    def create_summary(self, reporting: ReportingSummary) -> ReportingSummary | None:
        """
        Create a new reporting summary.
        """
        reporting_summary = ReportingSummaryDB(**reporting.model_dump())
        self.session.add(reporting_summary)
        self.session.commit()
        self.session.refresh(reporting_summary)    
        
        reporting_summary_dto = ReportingSummaryDTO.from_orm(reporting_summary)
             
        return ReportingSummary(**reporting_summary_dto.model_dump())
    
    def list_all_summaries(self) -> List[ReportingSummary] | None:
        """
        List all reporting summaries.
        """
        statement = select(ReportingSummaryDB)
        summaries = self.session.exec(statement).all()                                                  
        if not summaries:
            return None
        
        return [ReportingSummary(**ReportingSummaryDTO.from_orm(summary).__dict__) for summary in summaries]
    
    def get_grouped_summary(self) ->List[ReportingSummaryGrouped]:
        """
         Get a grouped summary of reporting data by school_name and class_name.
        """
        statement = (
        select(
            ReportingSummaryDB.school_name,
            ReportingSummaryDB.class_name,
            ReportingSummaryDB.is_certifying,
            func.sum(ReportingSummaryDB.nb_hours).label("total_hours"),
            func.max(ReportingSummaryDB.nb_students).label("total_students"), # only one value
            func.count().label("summary_count")
        )
        .group_by(
            ReportingSummaryDB.school_name, 
            ReportingSummaryDB.class_name,
            ReportingSummaryDB.is_certifying
        )
        .order_by(ReportingSummaryDB.school_name, ReportingSummaryDB.class_name)
    )

        results = self.session.exec(statement).all()

        if not results:
            return []

        return [
            ReportingSummaryGrouped(
                school_name=school_name,
                class_name=class_name,
                is_certifying=is_certifying,
                total_hours=total_hours,
                total_students=total_students,
                summary_count=summary_count,
        )
            for school_name, class_name, is_certifying, total_hours, total_students, summary_count in results
    ]
        
    def get_totals_by_certification(self) -> TotalsByCertificationDTO:
        grouped = self.get_grouped_summary()

        certifying = [item for item in grouped if item.is_certifying]
        not_certifying = [item for item in grouped if not item.is_certifying]

        # Comptage des enseignants distincts
        
        statement = (
                select(
                    func.count(func.distinct(
                        func.lower(func.trim(func.replace(ReportingSummaryDB.teacher_name, '  ', ' ')))
                    ))
                )
                .where(ReportingSummaryDB.teacher_name.is_not(None))
            )
        number_of_teachers = self.session.exec(statement).one() or 0
        
        certifying_totals = CertificationTotalsDTO(
            total_hours=sum(item.total_hours for item in certifying),
            total_students=sum(item.total_students for item in certifying),
            group_count=len(certifying)
        )

        not_certifying_totals = CertificationTotalsDTO(
            total_hours=sum(item.total_hours for item in not_certifying),
            total_students=sum(item.total_students for item in not_certifying),
            group_count=len(not_certifying)
        )

        return TotalsByCertificationDTO(
            certifying=certifying_totals,
            not_certifying=not_certifying_totals,
            number_of_teachers=int(number_of_teachers),
        )
        
    def get_last_invoice_name(self) -> int:
        """
        Get the last invoice name.
        """
        statement = select(func.min(ReportingSummaryDB.invoice_name))
        last_invoice = self.session.exec(statement).one()
        
        if last_invoice is None:
            return 0
        
        return int(last_invoice) 
        
    def get_filtered_summaries(self, filters: ReportingSummaryFilterDTO) -> List[ReportingSummary]:
        statement = select(ReportingSummaryDB)
        
        if filters.school_name:
            statement = statement.where(ReportingSummaryDB.school_name == filters.school_name)
        if filters.class_name:
            statement = statement.where(ReportingSummaryDB.class_name == filters.class_name)
        if filters.teacher_name:
            statement = statement.where(ReportingSummaryDB.teacher_name == filters.teacher_name)
        if filters.invoice_name:
            statement = statement.where(ReportingSummaryDB.invoice_name == filters.invoice_name)
        if filters.is_certifying is not None:
            statement = statement.where(ReportingSummaryDB.is_certifying == filters.is_certifying)
        
        if filters.min_hours is not None:
            statement = statement.where(ReportingSummaryDB.nb_hours >= filters.min_hours)
        if filters.max_hours is not None:
            statement = statement.where(ReportingSummaryDB.nb_hours <= filters.max_hours)
        
        if filters.min_students is not None:
            statement = statement.where(ReportingSummaryDB.nb_students >= filters.min_students)
        if filters.max_students is not None:
            statement = statement.where(ReportingSummaryDB.nb_students <= filters.max_students)
        
        if filters.start_date:
            statement = statement.where(ReportingSummaryDB.billed_at >= filters.start_date)
        if filters.end_date:
            statement = statement.where(ReportingSummaryDB.billed_at <= filters.end_date)
        
        summaries = self.session.exec(statement).all()
        if not summaries:
            return []
        
        return [ReportingSummary(**ReportingSummaryDTO.from_orm(s).__dict__) for s in summaries]
    

    def normalize_teacher_name(name: str) -> str:
            # Supprime les espaces inutiles et met en minuscule
            return " ".join(name.strip().split()).lower()