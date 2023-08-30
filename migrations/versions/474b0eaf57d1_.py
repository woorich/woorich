"""empty message

Revision ID: 474b0eaf57d1
Revises: 
Create Date: 2023-08-30 11:51:18.399489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '474b0eaf57d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('no', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.String(length=45), nullable=False),
    sa.Column('admin_pw', sa.String(length=45), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('no', name=op.f('pk_admin')),
    sa.UniqueConstraint('admin_id', name=op.f('uq_admin_admin_id'))
    )
    op.create_table('user',
    sa.Column('no', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=45), nullable=False),
    sa.Column('user_pw', sa.String(length=45), nullable=False),
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('email', sa.String(length=45), nullable=False),
    sa.Column('phone', sa.String(length=45), nullable=False),
    sa.Column('address', sa.String(length=45), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('no', name=op.f('pk_user')),
    sa.UniqueConstraint('address', name=op.f('uq_user_address')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('phone', name=op.f('uq_user_phone')),
    sa.UniqueConstraint('user_id', name=op.f('uq_user_user_id'))
    )
    op.create_table('board',
    sa.Column('no', sa.Integer(), nullable=False),
    sa.Column('b_title', sa.String(length=45), nullable=False),
    sa.Column('b_content', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_no', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_no'], ['user.no'], name=op.f('fk_board_user_no_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('no', name=op.f('pk_board'))
    )
    op.create_table('history',
    sa.Column('no', sa.Integer(), nullable=False),
    sa.Column('region', sa.String(length=45), nullable=False),
    sa.Column('job_type', sa.String(length=45), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('link', sa.String(length=200), nullable=False),
    sa.Column('user_no', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_no'], ['user.no'], name=op.f('fk_history_user_no_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('no', name=op.f('pk_history'))
    )
    op.create_table('reply',
    sa.Column('no', sa.Integer(), nullable=False),
    sa.Column('r_content', sa.String(length=45), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('admin_no', sa.Integer(), nullable=True),
    sa.Column('board_no', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_no'], ['admin.no'], name=op.f('fk_reply_admin_no_admin'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['board_no'], ['board.no'], name=op.f('fk_reply_board_no_board'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('no', name=op.f('pk_reply'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reply')
    op.drop_table('history')
    op.drop_table('board')
    op.drop_table('user')
    op.drop_table('admin')
    # ### end Alembic commands ###
