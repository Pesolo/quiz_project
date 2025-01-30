"""Allow NULL values for difficulty in QuizAttempt

Revision ID: 9684bb9ac987
Revises: 9d5cb0d2c5af
Create Date: 2025-01-26 23:48:40.282630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9684bb9ac987'
down_revision = '9d5cb0d2c5af'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Handle quiz_attempt table changes
    op.alter_column('quiz_attempt', 'difficulty',
                    existing_type=sa.VARCHAR(length=20),
                    nullable=True)
    
    op.execute("UPDATE quiz_attempt SET difficulty = 'Easy' WHERE difficulty IS NULL")
    
    op.alter_column('quiz_attempt', 'difficulty',
                    existing_type=sa.VARCHAR(length=20),
                    nullable=False)

    # 2. Handle certificate table changes
    # First ensure the column is nullable (in case it isn't already)
    op.alter_column('certificate', 'category',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)
    
    # Set a default value for existing NULL entries
    # Replace 'general' with whatever default category makes sense for your application
    op.execute("UPDATE certificate SET category = 'general' WHERE category IS NULL")
    
    # Now it's safe to set the NOT NULL constraint
    op.alter_column('certificate', 'category',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=False)

def downgrade():
    # Allow rollback by making columns nullable again
    op.execute("UPDATE certificate SET category = 'General' WHERE category IS NULL")

    # Allow rollback by making category nullable again
    op.alter_column('certificate', 'category',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)

    # Allow rollback by making difficulty nullable again
    op.alter_column('quiz_attempt', 'difficulty',
                    existing_type=sa.VARCHAR(length=20),
                    nullable=True)