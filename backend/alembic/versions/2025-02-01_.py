"""empty message

Revision ID: 7098ee78ca61
Revises: 
Create Date: 2025-02-01 00:00:44.561164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7098ee78ca61'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('business',
    sa.Column('business_name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('fair',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_day', sa.DateTime(), nullable=False),
    sa.Column('end_day', sa.DateTime(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('payment',
    sa.Column('payment_status', sa.String(), nullable=False),
    sa.Column('payment_stripe_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('place',
    sa.Column('place_name', sa.String(length=50), nullable=False),
    sa.Column('place_zona', sa.INTEGER(), nullable=True),
    sa.Column('place_cordinates', sa.String(length=50), nullable=True),
    sa.Column('place_reservated', sa.BOOLEAN(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('place_cordinates')
    )
    op.create_table('fair_place_association',
    sa.Column('fair_id', sa.UUID(), nullable=True),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['fair_id'], ['fair.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], )
    )
    op.create_table('reservation',
    sa.Column('business_id', sa.UUID(), nullable=True),
    sa.Column('payment_id', sa.UUID(), nullable=True),
    sa.Column('fair_id', sa.UUID(), nullable=True),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['fair_id'], ['fair.id'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fair_id', 'place_id', name='uq_reservation_fair_place'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('payment_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    op.drop_table('fair_place_association')
    op.drop_table('place')
    op.drop_table('payment')
    op.drop_table('fair')
    op.drop_table('business')
    op.drop_table('admin')
    # ### end Alembic commands ###
