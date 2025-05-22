from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid
from datetime import datetime

from faker import Faker

# revision identifiers
revision: str = '1509304d5a16'
down_revision: Union[str, None] = 'fd2b7cddd8c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'reporting_summary',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('invoice_name', sa.Integer(), nullable=False),
        sa.Column('nb_hours', sa.Float(), nullable=False),
        sa.Column('nb_students', sa.Integer(), nullable=False),
        sa.Column('school_name', sa.String(), nullable=False),
        sa.Column('class_name', sa.String(), nullable=True),
        sa.Column('teacher_name', sa.String(), nullable=True),
        sa.Column('billed_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    # --- Insert fake data
    bind = op.get_bind()
    faker = Faker()

    sample_data = [
        {
            "id": str(uuid.uuid4()),
            "invoice_name": faker.random_int(min=1000, max=9999),
            "nb_hours": round(faker.random_number(digits=2) / 2, 1),
            "nb_students": faker.random_int(min=10, max=35),
            "school_name": faker.company(),
            "class_name": faker.bothify(text='Classe ???'),
            "teacher_name": faker.name(),
            "billed_at": datetime.now(),
            "created_at": datetime.now()
        },
        {
            "id": str(uuid.uuid4()),
            "invoice_name": faker.random_int(min=1000, max=9999),
            "nb_hours": round(faker.random_number(digits=2) / 2, 1),
            "nb_students": faker.random_int(min=10, max=35),
            "school_name": faker.company(),
            "class_name": faker.bothify(text='Classe ???'),
            "teacher_name": faker.name(),
            "created_at": datetime.utcnow()
        }
    ]

    bind.execute(sa.text("""
        INSERT INTO reporting_summary (
            id, invoice_name, nb_hours, nb_students, school_name,
            class_name, teacher_name, created_at
        ) VALUES (
            :id, :invoice_name, :nb_hours, :nb_students, :school_name,
            :class_name, :teacher_name, :created_at
        )
    """), sample_data)

def downgrade():
    op.drop_table('reporting_summary')
