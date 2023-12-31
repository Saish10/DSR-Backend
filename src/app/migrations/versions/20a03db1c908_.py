"""empty message

Revision ID: 20a03db1c908
Revises: 27d374f4bed2
Create Date: 2023-12-31 15:57:33.156351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20a03db1c908'
down_revision = '27d374f4bed2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_token', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.Text(), nullable=True))
        batch_op.drop_index('ix_auth_token_access_token')
        batch_op.drop_index('ix_auth_token_refresh_token')
        batch_op.create_index(batch_op.f('ix_auth_token_token'), ['token'], unique=False)
        batch_op.drop_column('refresh_token')
        batch_op.drop_column('access_token')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_token', schema=None) as batch_op:
        batch_op.add_column(sa.Column('access_token', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('refresh_token', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.drop_index(batch_op.f('ix_auth_token_token'))
        batch_op.create_index('ix_auth_token_refresh_token', ['refresh_token'], unique=False)
        batch_op.create_index('ix_auth_token_access_token', ['access_token'], unique=False)
        batch_op.drop_column('token')

    # ### end Alembic commands ###
