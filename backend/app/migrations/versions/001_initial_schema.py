"""
Initial Schema Migration
Create core tables for maritime route planning.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create initial database schema."""
    
    # Enable PostGIS extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    # Create ports table
    op.create_table(
        'ports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('unlocode', sa.String(5), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('country', sa.String(100), nullable=False),
        sa.Column('latitude', sa.Numeric(10, 7), nullable=False),
        sa.Column('longitude', sa.Numeric(11, 7), nullable=False),
        sa.Column('port_type', sa.String(50)),
        sa.Column('max_draft', sa.Numeric(6, 2)),
        sa.Column('max_vessel_length', sa.Numeric(8, 2)),
        sa.Column('facilities', sa.JSON()),
        sa.Column('operational_status', sa.String(20), default='active'),
        sa.Column('timezone', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create routes table
    op.create_table(
        'routes',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('origin_port_id', sa.Integer(), sa.ForeignKey('ports.id')),
        sa.Column('destination_port_id', sa.Integer(), sa.ForeignKey('ports.id')),
        sa.Column('waypoints', sa.JSON()),
        sa.Column('total_distance_nm', sa.Numeric(12, 2)),
        sa.Column('estimated_duration_hours', sa.Numeric(10, 2)),
        sa.Column('optimization_criteria', sa.String(50)),
        sa.Column('calculated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create vessels table
    op.create_table(
        'vessels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('imo_number', sa.String(10), unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('vessel_type', sa.String(50)),
        sa.Column('length_meters', sa.Numeric(8, 2)),
        sa.Column('beam_meters', sa.Numeric(6, 2)),
        sa.Column('draft_meters', sa.Numeric(5, 2)),
        sa.Column('max_speed_knots', sa.Numeric(5, 2)),
        sa.Column('fuel_type', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    """Remove tables."""
    op.drop_table('vessels')
    op.drop_table('routes')
    op.drop_table('ports')
