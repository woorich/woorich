"""Added is_admin column

Revision ID: 36f1598a52af
Revises: 68cd9ccd31b2
Create Date: 2023-09-15 13:17:41.029505

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '36f1598a52af'
down_revision = '68cd9ccd31b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.alter_column('b_title',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('b_content',
               existing_type=mysql.VARCHAR(length=500),
               type_=sa.String(length=5000),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=False))
        batch_op.alter_column('address',
               existing_type=mysql.VARCHAR(length=45),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=45),
               existing_nullable=False)
        batch_op.drop_column('is_admin')

    with op.batch_alter_table('board', schema=None) as batch_op:
        batch_op.alter_column('b_content',
               existing_type=sa.String(length=5000),
               type_=mysql.VARCHAR(length=500),
               existing_nullable=False)
        batch_op.alter_column('b_title',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=45),
               existing_nullable=False)

    # ### end Alembic commands ###
