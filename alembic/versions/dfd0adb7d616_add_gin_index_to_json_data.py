"""Add GIN index to json_data

Revision ID: dfd0adb7d616
Revises: 117cdc597705
Create Date: 2025-01-08 12:07:04.151322

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = 'dfd0adb7d616'
down_revision = '117cdc597705'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Изменяем тип данных json_data на JSONB
    op.alter_column('sessions', 'json_data', type_=sa.dialects.postgresql.JSONB)

    # Создаем GIN индекс для json_data
    op.execute(
        "CREATE INDEX idx_sessions_json_data_gin ON sessions USING gin (json_data gin_trgm_ops)"
    )


def downgrade() -> None:
    # Удаляем GIN индекс
    op.execute("DROP INDEX IF EXISTS idx_sessions_json_data_gin")

    # Возвращаем тип данных json_data на JSON
    op.alter_column('sessions', 'json_data', type_=sa.JSON)
