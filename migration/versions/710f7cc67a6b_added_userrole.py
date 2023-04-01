"""Added UserRole

Revision ID: 710f7cc67a6b
Revises: 62d9efb52c46
Create Date: 2023-04-01 19:08:48.671851

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '710f7cc67a6b'
down_revision = '62d9efb52c46'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transform_posts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('photo_url', sa.String(), nullable=False),
                    sa.Column('photo_id', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['photo_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    role_enum = postgresql.ENUM(
        'Admin', 'Moderator', 'User', name='userrole', create_type=False)
    role_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('users', sa.Column('user_role', role_enum, nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_role')
    op.drop_column('users', 'is_active')
    op.drop_table('transform_posts')
    # ### end Alembic commands ###
