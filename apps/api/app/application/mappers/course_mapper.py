from domain.models.Course import Course
from application.dtos.course_dto import CourseDTO
from infrastructure.db.models.CourseDB import CourseDB

def course_db_to_domain(course_db: CourseDB ) -> Course:
    return Course(
        id=course_db.id,
        title=course_db.title,
        content=course_db.content,
        is_published=course_db.is_published,
        created_at=course_db.created_at,
        updated_at=course_db.updated_at,
        author_ids=[author.id for author in course_db.authors],
    )

def course_domain_to_dto(course) -> CourseDTO:
    return CourseDTO(
        id=course.id,
        title=course.title,
        content=course.content,
        is_published=course.is_published,
        created_at=course.created_at,
        updated_at=course.updated_at,
        author_ids=course.author_ids,
    )
