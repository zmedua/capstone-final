from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=2),
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=2),
    )

    muscle_group = fields.Str(
        allow_none=True,
        validate=validate.Length(min=2),
    )

    equipment = fields.Str(
        allow_none=True,
        validate=validate.Length(min=2),
    )

    difficulty = fields.Str(
        allow_none=True,
        validate=validate.OneOf(
            [
                "beginner",
                "intermediate",
                "advanced",
            ]
        ),
    )

    description = fields.Str(allow_none=True)

    
    external_id = fields.Str(allow_none=True)
    image_url = fields.Str(allow_none=True)

    workout_exercises = fields.List(
        fields.Nested(
            lambda: WorkoutExerciseSchema(
                exclude=("exercise",)
            )
        ),
        dump_only=True,
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1),
    )

    notes = fields.Str(allow_none=True)

    
    completed = fields.Bool(load_default=False)

    completed_at = fields.DateTime(
        allow_none=True,
        dump_only=True,
    )

    user_id = fields.Int(dump_only=True)

    workout_exercises = fields.List(
        fields.Nested(
            lambda: WorkoutExerciseSchema(
                exclude=("workout",)
            )
        ),
        dump_only=True,
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )

    weight = fields.Float(
        allow_none=True,
        validate=validate.Range(min=0),
    )

    duration_minutes = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )

    workout = fields.Nested(
        lambda: WorkoutSchema(
            exclude=("workout_exercises",)
        ),
        dump_only=True,
    )

    exercise = fields.Nested(
        lambda: ExerciseSchema(
            exclude=("workout_exercises",)
        ),
        dump_only=True,
    )

    @validates_schema
    def validate_tracking_data(self, data, **kwargs):
        reps = data.get("reps")
        sets = data.get("sets")
        duration_minutes = data.get("duration_minutes")
        weight = data.get("weight")

        has_strength_data = (
            reps is not None or
            sets is not None or
            weight is not None
        )

        has_cardio_data = duration_minutes is not None

        if not has_strength_data and not has_cardio_data:
            raise ValidationError(
                "Include sets and reps for a strength exercise "
                "or duration_minutes for a cardio exercise."
            )

        if has_strength_data:
            missing_fields = {}

            if reps is None:
                missing_fields["reps"] = [
                    "Reps are required for strength exercises."
                ]

            if sets is None:
                missing_fields["sets"] = [
                    "Sets are required for strength exercises."
                ]

            if missing_fields:
                raise ValidationError(missing_fields)


class FavoriteExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    exercise = fields.Nested(
        ExerciseSchema,
        dump_only=True,
    )