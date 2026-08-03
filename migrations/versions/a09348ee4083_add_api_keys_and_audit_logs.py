"""add_api_keys_and_audit_logs

Revision ID: a09348ee4083
Revises: 31f3a745de49
Create Date: 2026-06-12 11:53:19.782981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a09348ee4083'
down_revision: Union[str, None] = '31f3a745de49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create `api_keys` table
    op.create_table(
        "api_keys",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("owner_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_api_keys_key'), 'api_keys', ['key'], unique=False)

    # Create `audit_logs` table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("method", sa.String(length=10), nullable=False),
        sa.Column("path", sa.String(length=500), nullable=False),
        sa.Column("api_key_owner", sa.String(length=255), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("client_host", sa.String(length=100), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('ix_audit_timestamp', 'audit_logs', ['timestamp'])
    op.create_index('ix_audit_owner', 'audit_logs', ['api_key_owner'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_audit_owner', table_name='audit_logs')
    op.drop_index('ix_audit_timestamp', table_name='audit_logs')
    op.drop_table('audit_logs')

    op.drop_index(op.f('ix_api_keys_key'), table_name='api_keys')
    op.drop_table('api_keys')
    # ### end Alembic commands ###
