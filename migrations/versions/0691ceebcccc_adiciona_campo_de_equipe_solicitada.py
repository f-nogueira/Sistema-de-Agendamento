"""Adiciona campo de equipe solicitada

Revision ID: 0691ceebcccc
Revises: aad28c4412e4
Create Date: 2025-09-29 11:42:56.033530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0691ceebcccc'
down_revision = 'aad28c4412e4'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona o comando para criar a coluna
    with op.batch_alter_table('agendamento', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mesa_portatil', sa.Boolean(), server_default=sa.text('0'), nullable=False))


def downgrade():
    # Adiciona o comando para remover a coluna (caso precise reverter)
    with op.batch_alter_table('agendamento', schema=None) as batch_op:
        batch_op.drop_column('mesa_portatil')
