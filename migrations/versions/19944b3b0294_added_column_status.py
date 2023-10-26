"""Added column status

Revision ID: 19944b3b0294
Revises: 82f07b477160
Create Date: 2023-10-27 00:45:57.240128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19944b3b0294'
down_revision: Union[str, None] = '82f07b477160'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('computers', sa.Column('status', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('computers', 'status')
    # ### end Alembic commands ###
