"""empty message

Revision ID: 7117d316e171
Revises: 
Create Date: 2023-02-18 14:26:17.702571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7117d316e171'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family_member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=200), nullable=False),
    sa.Column('data_created', sa.DateTime(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('FamilyMember_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    op.drop_table('family_member')
    # ### end Alembic commands ###