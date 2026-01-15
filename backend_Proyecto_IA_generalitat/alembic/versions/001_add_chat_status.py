"""add chat status and completed_at fields

Revision ID: 001_add_chat_status
Revises: 
Create Date: 2024-01-15 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_add_chat_status'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add status and completed_at columns to chats table"""
    # Add status column with default value 'active'
    op.add_column('chats', 
        sa.Column('status', sa.String(20), server_default='active', nullable=False)
    )
    
    # Add completed_at column (nullable for active chats)
    op.add_column('chats', 
        sa.Column('completed_at', sa.DateTime, nullable=True)
    )
    
    # Create index on status for faster queries
    op.create_index('ix_chats_status', 'chats', ['status'])


def downgrade() -> None:
    """Remove status and completed_at columns from chats table"""
    op.drop_index('ix_chats_status', table_name='chats')
    op.drop_column('chats', 'completed_at')
    op.drop_column('chats', 'status')
