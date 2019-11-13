"""empty message

Revision ID: c74576b4a43a
Revises: a78a3b57a169
Create Date: 2019-11-13 15:20:49.732948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c74576b4a43a'
down_revision = 'a78a3b57a169'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('video', 'description',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=2000),
               existing_nullable=True)
    op.alter_column('video', 'url',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=250),
               existing_nullable=True)
    op.alter_column('videographer', 'bio',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=2000),
               existing_nullable=True)
    op.alter_column('videographer', 'profile_url',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=250),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('videographer', 'profile_url',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
    op.alter_column('videographer', 'bio',
               existing_type=sa.String(length=2000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
    op.alter_column('video', 'url',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
    op.alter_column('video', 'description',
               existing_type=sa.String(length=2000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
    # ### end Alembic commands ###
