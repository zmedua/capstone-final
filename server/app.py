from flask import Flask, request, make_response, session
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, bcrypt, User, Exercise, Workout, WorkoutExercise, FavoriteExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema, FavoriteExerciseSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "secret-key"
bcrypt.init_app(app)

migrate = Migrate(app, db)
db.init_app(app)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
favorite_exercise_schema = FavoriteExerciseSchema()
favorite_exercises_schema = FavoriteExerciseSchema(many=True)
@app.route("/workouts", methods=["GET"])
def get_workouts():
    user_id = session.get("user_id")
    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)
    
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = Workout.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return make_response({
        "workouts": workouts_schema.dump(pagination.items),
        "page": page,
        "per_page": per_page,
        "total":pagination.total,
        "pages": pagination.pages
    }, 200)

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    user_id = session.get("user_id")
    if not user_id:
        return make_response({"error":"Unauthorized"}, 401)
    
    workout = Workout.query.filter_by(id=id, user_id=user_id).first()

    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    return make_response(workout_schema.dump(workout), 200)

@app.route("/workouts", methods=["POST"])
def create_workout():
    if not session.get("user_id"):
        return make_response({"error": "Unauthorized"}, 401)
    try:
        data = workout_schema.load(request.get_json() or {})

        workout = Workout(
            date=data["date"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes"),
            completed=data.get("completed", False),
            user_id=session["user_id"]

        )

        db.session.add(workout)
        db.session.commit()

        return make_response(workout_schema.dump(workout), 201)
    
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)
    
    except ValueError as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    user_id = session.get("user_id")
    if not user_id:
        return make_response({"error":"Unauthorized"}, 401)
    workout = Workout.query.filter_by(id=id, user_id=user_id).first()

    if not workout:
        return make_response({"error": "Workout not found"}, 404)
   
    db.session.delete(workout)
    db.session.commit()

    return make_response({}, 204)
@app.route("/workouts/<int:id>", methods=["PATCH"])
def update_workout(id):
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)
    
    workout = Workout.query.filter_by(id=id, user_id=user_id).first()

    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    data = request.get_json()
    if "date" in data:
        workout.date = workout_schema.load({"date": data["date"], "duration_minutes": workout.duration_minutes})["date"]
    if "duration_minutes" in data:
        workout.duration_minutes = data["duration_minutes"]
    if "notes" in data:
        workout.notes = data["notes"]
    db.session.commit()

    return make_response(workout_schema.dump(workout), 200)
@app.route("/workouts/<int:id>/complete", methods=["PATCH"])
def complete_workout(id):
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    workout = Workout.query.filter_by(
        id=id,
        user_id=user_id,
    ).first()

    if not workout:
        return make_response(
            {"error": "Workout not found"},
            404,
        )

    workout.mark_complete()

    db.session.commit()

    return make_response(
        workout_schema.dump(workout),
        200,
    )
@app.route("/workouts/<int:id>/incomplete", methods=["PATCH"])
def mark_workout_incomplete(id):
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    workout = Workout.query.filter_by(
        id=id,
        user_id=user_id,
    ).first()

    if not workout:
        return make_response(
            {"error": "Workout not found"},
            404,
        )

    workout.mark_incomplete()

    db.session.commit()

    return make_response(
        workout_schema.dump(workout),
        200,
    )
@app.route("/workouts/history", methods=["GET"])
def get_workout_history():
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    completed_workouts = (
        Workout.query
        .filter_by(
            user_id=user_id,
            completed=True,
        )
        .order_by(Workout.completed_at.desc())
        .all()
    )

    return make_response(
        workouts_schema.dump(completed_workouts),
        200,
    )
@app.route("/workouts/upcoming", methods=["GET"])
def get_upcoming_workouts():
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    workouts = (
        Workout.query
        .filter_by(
            user_id=user_id,
            completed=False,
        )
        .order_by(Workout.date.asc())
        .all()
    )

    return make_response(
        workouts_schema.dump(workouts),
        200,
    )
@app.route("/exercises", methods=["GET"])
def get_exercises():
    search = request.args.get(
        "search",
        type=str,
    )

    category = request.args.get(
        "category",
        type=str,
    )

    muscle_group = request.args.get(
        "muscle_group",
        type=str,
    )

    equipment = request.args.get(
        "equipment",
        type=str,
    )

    difficulty = request.args.get(
        "difficulty",
        type=str,
    )

    query = Exercise.query

    if search:
        cleaned_search = search.strip()

        query = query.filter(
            Exercise.name.ilike(
                f"%{cleaned_search}%"
            )
        )

    if category and category.lower() != "all":
        query = query.filter(
            Exercise.category.ilike(category)
        )

    if muscle_group and muscle_group.lower() != "all":
        query = query.filter(
            Exercise.muscle_group.ilike(muscle_group)
        )

    if equipment and equipment.lower() != "all":
        query = query.filter(
            Exercise.equipment.ilike(equipment)
        )

    if difficulty and difficulty.lower() != "all":
        query = query.filter(
            Exercise.difficulty.ilike(difficulty)
        )

    exercises = query.order_by(
        Exercise.name.asc()
    ).all()

    return make_response(
        exercises_schema.dump(exercises),
        200,
    )
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    return make_response(exercise_schema.dump(exercise), 200)
@app.route("/favorites", methods=["GET"])
def get_favorite_exercises():
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    favorites = (
        FavoriteExercise.query
        .filter_by(user_id=user_id)
        .order_by(FavoriteExercise.created_at.desc())
        .all()
    )

    results = [
        {
            "id": favorite.id,
            "exercise": exercise_schema.dump(
                favorite.exercise
            ),
            "created_at": favorite.created_at.isoformat(),
        }
        for favorite in favorites
    ]

    return make_response(results, 200)
@app.route("/exercises", methods=["POST"])
def create_exercise():
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    try:
        data = exercise_schema.load(
            request.get_json() or {}
        )

        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            muscle_group=data.get("muscle_group"),
            equipment=data.get("equipment"),
            difficulty=data.get("difficulty"),
            description=data.get("description"),
            external_id=data.get("external_id"),
            image_url=data.get("image_url"),
        )

        db.session.add(exercise)
        db.session.commit()

        return make_response(
            exercise_schema.dump(exercise),
            201,
        )

    except ValidationError as error:
        return make_response(
            {"errors": error.messages},
            400,
        )

    except ValueError as error:
        db.session.rollback()

        return make_response(
            {"error": str(error)},
            400,
        )

    except IntegrityError:
        db.session.rollback()

        return make_response(
            {"error": "An exercise with this name already exists."},
            409,
        )
@app.route(
    "/favorites/<int:exercise_id>",
    methods=["POST"],
)
def add_favorite_exercise(exercise_id):
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    exercise = db.session.get(
        Exercise,
        exercise_id,
    )

    if not exercise:
        return make_response(
            {"error": "Exercise not found"},
            404,
        )

    existing_favorite = FavoriteExercise.query.filter_by(
        user_id=user_id,
        exercise_id=exercise_id,
    ).first()

    if existing_favorite:
        return make_response(
            {"error": "Exercise is already a favorite"},
            409,
        )

    favorite = FavoriteExercise(
        user_id=user_id,
        exercise_id=exercise_id,
    )

    db.session.add(favorite)
    db.session.commit()

    return make_response(
        {
            "id": favorite.id,
            "exercise": exercise_schema.dump(exercise),
            "created_at": favorite.created_at.isoformat(),
        },
        201,
    )
@app.route(
    "/favorites/<int:exercise_id>",
    methods=["DELETE"],
)
def delete_favorite_exercise(exercise_id):
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    favorite = FavoriteExercise.query.filter_by(
        user_id=user_id,
        exercise_id=exercise_id,
    ).first()

    if not favorite:
        return make_response(
            {"error": "Favorite exercise not found"},
            404,
        )

    db.session.delete(favorite)
    db.session.commit()

    return make_response("", 204)
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    
    db.session.delete(exercise)
    db.session.commit()

    return make_response({}, 204)

@app.route(
    "/workouts/<int:workout_id>/exercises/"
    "<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(
    workout_id,
    exercise_id,
):
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    workout = Workout.query.filter_by(
        id=workout_id,
        user_id=user_id,
    ).first()

    if not workout:
        return make_response(
            {"error": "Workout not found"},
            404,
        )

    exercise = db.session.get(
        Exercise,
        exercise_id,
    )

    if not exercise:
        return make_response(
            {"error": "Exercise not found"},
            404,
        )

    existing_entry = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id,
    ).first()

    if existing_entry:
        return make_response(
            {
                "error":
                "This exercise is already part of the workout."
            },
            409,
        )

    try:
        data = workout_exercise_schema.load(
            request.get_json() or {}
        )

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            weight=data.get("weight"),
            duration_minutes=data.get(
                "duration_minutes"
            ),
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return make_response(
            workout_exercise_schema.dump(
                workout_exercise
            ),
            201,
        )

    except ValidationError as error:
        return make_response(
            {"errors": error.messages},
            400,
        )

    except ValueError as error:
        db.session.rollback()

        return make_response(
            {"error": str(error)},
            400,
        )

    except IntegrityError:
        db.session.rollback()

        return make_response(
            {
                "error":
                "This exercise is already part of the workout."
            },
            409,
        )
@app.route(
    "/workout_exercises/<int:id>",
    methods=["DELETE"],
)
def delete_workout_exercise(id):
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)

    workout_exercise = (
        WorkoutExercise.query
        .join(
            Workout,
            WorkoutExercise.workout_id == Workout.id,
        )
        .filter(
            WorkoutExercise.id == id,
            Workout.user_id == user_id,
        )
        .first()
    )

    if not workout_exercise:
        return make_response(
            {"error": "Workout exercise not found"},
            404,
        )

    db.session.delete(workout_exercise)
    db.session.commit()

    return make_response("", 204)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return make_response({"errors": ["Username already exists"]}, 409)
    try:
        user = User(username=data.get("username"))
        user.password_hash = data.get("password")

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return make_response({
            "id": user.id,
            "username": user.username
        }, 201)

    except Exception as e:
        db.session.rollback()
        return make_response({"errors": [" error occured"]}, 400)
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter(User.username == data.get("username")).first()

    if user and user.authenticate(data.get("password")):
        session["user_id"] = user.id
        return make_response({
            "id": user.id,
            "username": user.username
        }, 200)
    return make_response({"error": "Invalid username or password"}, 401)
@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return make_response({}, 204)

@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return make_response({"error": "Unauthorized"}, 401)
    user = User.query.get(user_id)
    return make_response({
        "id": user.id,
        "username": user.username
    }, 200)
if __name__ == "__main__":
    app.run(port=5555, debug=True)