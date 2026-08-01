"""add workout history favorites and exercise fields

Revision ID: e93479f23e30
Revises: 6a60c81dbbee
Create Date: 2026-07-31 21:04:08.780977
"""

from alembic import op
import sqlalchemy as sa


revision = "e93479f23e30"
down_revision = "6a60c81dbbee"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "favorite_exercises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["exercise_id"],
            ["exercises.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "exercise_id",
            name="unique_favorite_exercise_per_user",
        ),
    )

    with op.batch_alter_table(
        "exercises",
        schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "muscle_group",
                sa.String(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "equipment",
                sa.String(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "difficulty",
                sa.String(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "description",
                sa.Text(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "external_id",
                sa.String(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "image_url",
                sa.String(),
                nullable=True,
            )
        )
        batch_op.create_unique_constraint(
            "uq_exercises_external_id",
            ["external_id"],
        )
        batch_op.drop_column("equipment_needed")

    with op.batch_alter_table(
        "workout_exercises",
        schema=None
    ) as batch_op:
        batch_op.drop_constraint(
            "check_duration_seconds_nonnegative",
            type_="check",
        )

        batch_op.add_column(
            sa.Column(
                "weight",
                sa.Float(),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "duration_minutes",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_check_constraint(
            "check_exercise_duration_nonnegative",
            "duration_minutes IS NULL OR "
            "duration_minutes >= 0",
        )

        batch_op.drop_column("duration_seconds")

    with op.batch_alter_table(
        "workouts",
        schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "completed",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )

        batch_op.add_column(
            sa.Column(
                "completed_at",
                sa.DateTime(),
                nullable=True,
            )
        )


def downgrade():
    with op.batch_alter_table(
        "workouts",
        schema=None
    ) as batch_op:
        batch_op.drop_column("completed_at")
        batch_op.drop_column("completed")

    with op.batch_alter_table(
        "workout_exercises",
        schema=None
    ) as batch_op:
        batch_op.drop_constraint(
            "check_exercise_duration_nonnegative",
            type_="check",
        )

        batch_op.add_column(
            sa.Column(
                "duration_seconds",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_check_constraint(
            "check_duration_seconds_nonnegative",
            "duration_seconds IS NULL OR "
            "duration_seconds >= 0",
        )

        batch_op.drop_column("duration_minutes")
        batch_op.drop_column("weight")

    with op.batch_alter_table(
        "exercises",
        schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "equipment_needed",
                sa.Boolean(),
                nullable=True,
            )
        )
        batch_op.drop_constraint(
            "uq_exercises_external_id",
            type_="unique",
        )
        batch_op.drop_column("image_url")
        batch_op.drop_column("external_id")
        batch_op.drop_column("description")
        batch_op.drop_column("difficulty")
        batch_op.drop_column("equipment")
        batch_op.drop_column("muscle_group")

    op.drop_table("favorite_exercises")