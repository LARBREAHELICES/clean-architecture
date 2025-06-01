from typing import List, Optional
from sqlmodel import select, func, Session

from app.domain.models.ReportingSummary import ReportingSummary, ReportingSummaryGrouped, CertificationTotals, TotalsByCertification
from app.infrastructure.db.models.ReportingSummaryDB import ReportingSummaryDB


class ReportingSummaryRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def create_summary(self, reporting: ReportingSummary) -> ReportingSummary:
        # Création d'une instance DB à partir des champs du modèle domaine (mapping manuel)
        reporting_db = ReportingSummaryDB(
            invoice_name=reporting.invoice_name,
            school_name=reporting.school_name,
            class_name=reporting.class_name,
            nb_hours=reporting.nb_hours,
            nb_students=reporting.nb_students,
            teacher_name=reporting.teacher_name,
            billed_at=reporting.billed_at,
            is_certifying=reporting.is_certifying,
        )
        self.session.add(reporting_db)
        self.session.commit()
        self.session.refresh(reporting_db)

        # Retourne un modèle domaine construit manuellement
        return ReportingSummary(
            id=reporting_db.id,
            invoice_name=reporting_db.invoice_name,
            school_name=reporting_db.school_name,
            class_name=reporting_db.class_name,
            nb_hours=reporting_db.nb_hours,
            nb_students=reporting_db.nb_students,
            teacher_name=reporting_db.teacher_name,
            billed_at=reporting_db.billed_at,
            is_certifying=reporting_db.is_certifying,
            created_at=reporting_db.created_at,
        )

    def list_all_summaries(self) -> List[ReportingSummary]:
        results = self.session.exec(select(ReportingSummaryDB)).all()
        return [
            ReportingSummary(
                id=r.id,
                invoice_name=r.invoice_name,
                school_name=r.school_name,
                class_name=r.class_name,
                nb_hours=r.nb_hours,
                nb_students=r.nb_students,
                teacher_name=r.teacher_name,
                billed_at=r.billed_at,
                is_certifying=r.is_certifying,
                created_at=r.created_at,
            )
            for r in results
        ]

    def get_grouped_summary(self) -> List[ReportingSummaryGrouped]:
        statement = (
            select(
                ReportingSummaryDB.school_name,
                ReportingSummaryDB.class_name,
                ReportingSummaryDB.is_certifying,
                func.sum(ReportingSummaryDB.nb_hours).label("total_hours"),
                func.max(ReportingSummaryDB.nb_students).label("total_students"),
                func.count().label("summary_count"),
            )
            .group_by(
                ReportingSummaryDB.school_name,
                ReportingSummaryDB.class_name,
                ReportingSummaryDB.is_certifying,
            )
            .order_by(ReportingSummaryDB.school_name, ReportingSummaryDB.class_name)
        )
        results = self.session.exec(statement).all()

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

    def get_totals_by_certification(self) -> CertificationTotals:
        grouped = self.get_grouped_summary()

        certifying = [item for item in grouped if item.is_certifying]
        not_certifying = [item for item in grouped if not item.is_certifying]

        statement = (
            select(
                func.count(
                    func.distinct(
                        func.lower(
                            func.trim(
                                func.replace(ReportingSummaryDB.teacher_name, "  ", " ")
                            )
                        )
                    )
                )
            )
            .where(ReportingSummaryDB.teacher_name.is_not(None))
        )
        number_of_teachers = self.session.exec(statement).one() or 0

        certifying_totals = CertificationTotals(
            total_hours=sum(item.total_hours for item in certifying),
            total_students=sum(item.total_students for item in certifying),
            group_count=len(certifying),
        )
        not_certifying_totals = CertificationTotals(
            total_hours=sum(item.total_hours for item in not_certifying),
            total_students=sum(item.total_students for item in not_certifying),
            group_count=len(not_certifying),
        )

        return TotalsByCertification(
           certifying=certifying_totals,
           not_certifying=not_certifying_totals,
           number_of_teachers= int(number_of_teachers)
        )

    def get_last_invoice_name(self) -> int:
        statement = select(func.min(ReportingSummaryDB.invoice_name))
        last_invoice = self.session.exec(statement).one()
        return int(last_invoice or 0)

    def get_filtered_summaries(self, filters) -> List[ReportingSummary]:
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

        return [
            ReportingSummary(
                id=s.id,
                invoice_name=s.invoice_name,
                school_name=s.school_name,
                class_name=s.class_name,
                nb_hours=s.nb_hours,
                nb_students=s.nb_students,
                teacher_name=s.teacher_name,
                billed_at=s.billed_at,
                is_certifying=s.is_certifying,
                created_at=s.created_at,
            )
            for s in summaries
        ]
