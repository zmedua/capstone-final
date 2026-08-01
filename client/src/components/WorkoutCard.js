import React, { useState } from "react";
import AddExerciseForm from "./AddExerciseForm";

function WorkoutCard({
  workout,
  exercises,
  onDeleteWorkout,
  onUpdateWorkout,
}) {
  const [error, setError] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [isUpdatingStatus, setIsUpdatingStatus] =
    useState(false);

  const workoutExercises =
    workout.workout_exercises || [];

  function handleDeleteWorkout() {
    setError("");
    setIsDeleting(true);

    fetch(`/workouts/${workout.id}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(
              data.error || "Unable to delete workout."
            );
          });
        }

        onDeleteWorkout(workout.id);
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setIsDeleting(false);
      });
  }

  function handleExerciseAdded(newWorkoutExercise) {
    const updatedWorkout = {
      ...workout,
      workout_exercises: [
        ...workoutExercises,
        newWorkoutExercise,
      ],
    };

    onUpdateWorkout(updatedWorkout);
  }

  function handleDeleteExercise(workoutExerciseId) {
    setError("");

    fetch(`/workout_exercises/${workoutExerciseId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(
              data.error || "Unable to remove exercise."
            );
          });
        }

        const updatedWorkout = {
          ...workout,
          workout_exercises: workoutExercises.filter(
            (workoutExercise) =>
              workoutExercise.id !== workoutExerciseId
          ),
        };

        onUpdateWorkout(updatedWorkout);
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  function handleCompleteWorkout() {
    setError("");
    setIsUpdatingStatus(true);

    fetch(`/workouts/${workout.id}/complete`, {
      method: "PATCH",
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(
              data.error ||
                "Unable to complete workout."
            );
          });
        }

        return response.json();
      })
      .then((updatedWorkout) => {
        onUpdateWorkout(updatedWorkout);
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setIsUpdatingStatus(false);
      });
  }

  function handleMarkIncomplete() {
    setError("");
    setIsUpdatingStatus(true);

    fetch(`/workouts/${workout.id}/incomplete`, {
      method: "PATCH",
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(
              data.error ||
                "Unable to update workout."
            );
          });
        }

        return response.json();
      })
      .then((updatedWorkout) => {
        onUpdateWorkout(updatedWorkout);
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setIsUpdatingStatus(false);
      });
  }

  return (
    <article className="workout-card">
      <h2>{workout.date}</h2>

      <p>
        Duration: {workout.duration_minutes} minutes
      </p>

      {workout.notes && <p>{workout.notes}</p>}

      <p>
        Status:{" "}
        <strong>
          {workout.completed
            ? "Completed"
            : "Upcoming"}
        </strong>
      </p>

      {workout.completed ? (
        <button
          className={
            workout.completed
              ? "incomplete-workout-button"
              : "complete-workout-button"
          }
          type="button"
          onClick={
            workout.completed
              ? handleMarkIncomplete
              : handleCompleteWorkout
          }
          disabled={isUpdatingStatus}
        >
          {isUpdatingStatus
            ? "Updating..."
            : workout.completed
              ? "Mark Incomplete"
              : "Complete Workout"}
        </button>
      ) : (
        <button
          type="button"
          onClick={handleCompleteWorkout}
          disabled={isUpdatingStatus}
        >
          {isUpdatingStatus
            ? "Updating..."
            : "Complete Workout"}
        </button>
      )}

      <h3>Exercises</h3>

      {workoutExercises.length === 0 ? (
        <p>No exercises have been added.</p>
      ) : (
        workoutExercises.map((workoutExercise) => {
          const exerciseName =
            workoutExercise.exercise?.name ||
            workoutExercise.exercise_name ||
            "Exercise";

          return (
            <div
              key={workoutExercise.id}
              className="workout-exercise"
            >
              <p>
                <strong>{exerciseName}</strong>

                {workoutExercise.sets != null &&
                workoutExercise.reps != null
                  ? ` — ${workoutExercise.sets} sets of ${workoutExercise.reps} reps`
                  : ""}

                {workoutExercise.weight != null
                  ? ` at ${workoutExercise.weight} lbs`
                  : ""}

                {workoutExercise.duration_minutes != null
                  ? ` — ${workoutExercise.duration_minutes} minutes`
                  : ""}
              </p>

              <button
                className="remove-exercise-button"
                type="button"
                onClick={() =>
                  handleDeleteExercise(
                    workoutExercise.id
                  )
                }
              >
                Remove Exercise
              </button>
            </div>
          );
        })
      )}

      {!workout.completed && (
        <AddExerciseForm
          workoutId={workout.id}
          exercises={exercises}
          onExerciseAdded={handleExerciseAdded}
        />
      )}

      <button
        className="delete-workout-button"
        type="button"
        onClick={handleDeleteWorkout}
        disabled={isDeleting}
      >
        {isDeleting
          ? "Deleting..."
          : "Delete Workout"}
      </button>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}
    </article>
  );
}

export default WorkoutCard;