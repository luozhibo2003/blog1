"""modify table link

Revision ID: 7b353311d142
Revises: ad8948d8dbd7
Create Date: 2019-04-19 16:35:04.072533

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7b353311d142'
down_revision = 'ad8948d8dbd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('link', sa.Column('name', sa.String(length=30), nullable=True))
    op.drop_column('link', 'name22')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('link', sa.Column('name22', mysql.VARCHAR(length=30), nullable=True))
    op.drop_column('link', 'name')
    # ### end Alembic commands ###
