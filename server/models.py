from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String,
        nullable=False,
        unique=True
    )
    _password_hash = db.Column(
        db.String,
        nullable=False
    )

    workouts = db.relationship(
        "Workout",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    favorite_exercise_records = db.relationship(
        "FavoriteExercise",
        back_populates="user",
        cascade="all, delete-orphan"
    )

  
    favorite_exercises = association_proxy(
        "favorite_exercise_records",
        "exercise"
    )

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        if not password or len(password) < 6:
            raise ValueError(
                "Password must be at least 6 characters."
            )

        generated_hash = bcrypt.generate_password_hash(
            password.encode("utf-8")
        )

        self._password_hash = generated_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password.encode("utf-8")
        )

    @validates("username")
    def validate_username(self, key, username):
        if not username or len(username.strip()) < 3:
            raise ValueError(
                "Username must be at least 3 characters."
            )

        return username.strip()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    category = db.Column(
        db.String,
        nullable=False
    )

    
    muscle_group = db.Column(db.String)
    equipment = db.Column(db.String)
    difficulty = db.Column(db.String)

    description = db.Column(db.Text)

    
    external_id = db.Column(db.String)
    image_url = db.Column(db.String)

    __table_args__ = (
        UniqueConstraint(
            "external_id",
            name="uq_exercises_external_id"
        ),
    )
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = association_proxy(
        "workout_exercises",
        "workout"
    )

    favorite_records = db.relationship(
        "FavoriteExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    users_who_favorited = association_proxy(
        "favorite_records",
        "user"
    )

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError(
                "Exercise name must be at least 2 characters."
            )

        return name.strip()

    @validates("category")
    def validate_category(self, key, category):
        if not category or len(category.strip()) < 2:
            raise ValueError("Please enter a category.")

        return category.strip()

    @validates("difficulty")
    def validate_difficulty(self, key, difficulty):
        if difficulty is None:
            return None

        allowed_difficulties = {
            "beginner",
            "intermediate",
            "advanced"
        }

        cleaned_difficulty = difficulty.strip().lower()

        if cleaned_difficulty not in allowed_difficulties:
            raise ValueError(
                "Difficulty must be beginner, intermediate, "
                "or advanced."
            )

        return cleaned_difficulty


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(
        db.Date,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    notes = db.Column(db.Text)

    # New workout-history fields
    completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="workouts"
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = association_proxy(
        "workout_exercises",
        "exercise"
    )

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="check_duration_positive"
        ),
    )

    @validates("duration_minutes")
    def validate_duration(self, key, duration_minutes):
        if duration_minutes is None or duration_minutes <= 0:
            raise ValueError(
                "Workout duration must be greater than 0."
            )

        return duration_minutes

    def mark_complete(self):
        self.completed = True
        self.completed_at = datetime.utcnow()

    def mark_incomplete(self):
        self.completed = False
        self.completed_at = None


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)

    # New field for strength exercises
    weight = db.Column(db.Float)

    # Using minutes may be clearer for cardio workouts.
    duration_minutes = db.Column(db.Integer)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    __table_args__ = (
        CheckConstraint(
            "reps IS NULL OR reps >= 0",
            name="check_reps_nonnegative"
        ),
        CheckConstraint(
            "sets IS NULL OR sets >= 0",
            name="check_sets_nonnegative"
        ),
        CheckConstraint(
            "weight IS NULL OR weight >= 0",
            name="check_weight_nonnegative"
        ),
        CheckConstraint(
            "duration_minutes IS NULL OR duration_minutes >= 0",
            name="check_exercise_duration_nonnegative"
        ),
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_exercise_per_workout"
        ),
    )

    @validates(
        "reps",
        "sets",
        "weight",
        "duration_minutes"
    )
    def validate_nonnegative(self, key, value):
        if value is not None and value < 0:
            raise ValueError(
                f"{key.replace('_', ' ').title()} cannot be negative."
            )

        return value


class FavoriteExercise(db.Model):
    __tablename__ = "favorite_exercises"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="favorite_exercise_records"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="favorite_records"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "exercise_id",
            name="unique_favorite_exercise_per_user"
        ),
    )