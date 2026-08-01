from datetime import date

from app import app
from models import (
    db,
    User,
    Exercise,
    Workout,
    WorkoutExercise,
    FavoriteExercise,
)


with app.app_context():
    FavoriteExercise.query.delete()
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    User.query.delete()

    user = User(username="zanemedua")
    user.password_hash = "password123"

    db.session.add(user)
    db.session.commit()

    bench_press = Exercise(
        name="Bench Press",
        category="Strength",
        muscle_group="Chest",
        equipment="Barbell",
        difficulty="beginner",
        description="A strength exercise that targets the chest.",
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        muscle_group="Legs",
        equipment="Bodyweight",
        difficulty="beginner",
        description="A lower-body exercise that targets the legs.",
    )

    treadmill = Exercise(
        name="Treadmill Run",
        category="Cardio",
        muscle_group="Legs",
        equipment="Treadmill",
        difficulty="beginner",
        description="A cardio exercise performed on a treadmill.",
    )

    workout1 = Workout(
        date=date(2026, 6, 20),
        duration_minutes=45,
        notes="Upper body and cardio",
        completed=False,
        user_id=user.id,
    )

    workout2 = Workout(
        date=date(2026, 6, 21),
        duration_minutes=30,
        notes="Leg day",
        completed=False,
        user_id=user.id,
    )

    db.session.add_all([
        bench_press,
        squats,
        treadmill,
        workout1,
        workout2,
    ])
    db.session.commit()

    we1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=bench_press.id,
        reps=8,
        sets=3,
        weight=135,
    )

    we2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=treadmill.id,
        duration_minutes=15,
    )

    we3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=squats.id,
        reps=12,
        sets=4,
        weight=95,
    )

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeded")