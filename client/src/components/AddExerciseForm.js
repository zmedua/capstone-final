import React, { useState } from "react";

function AddExerciseForm({
  workoutId,
  exercises,
  onExerciseAdded,
}) {
  const [exerciseId, setExerciseId] = useState("");
  const [sets, setSets] = useState("");
  const [reps, setReps] = useState("");
  const [weight, setWeight] = useState("");
  const [durationMinutes, setDurationMinutes] =
    useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const selectedExercise = exercises.find(
    (exercise) => exercise.id === Number(exerciseId)
  );

  const isCardio =
    selectedExercise?.category?.toLowerCase() === "cardio";

  function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    const body = isCardio
      ? {
          duration_minutes: Number(durationMinutes),
        }
      : {
          sets: Number(sets),
          reps: Number(reps),
          weight: weight ? Number(weight) : null,
        };

    fetch(
      `/workouts/${workoutId}/exercises/${exerciseId}/workout_exercises`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    )
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(
              data.error || "Unable to add exercise."
            );
          });
        }

        return response.json();
      })
      .then((newWorkoutExercise) => {
        onExerciseAdded(newWorkoutExercise);

        setExerciseId("");
        setSets("");
        setReps("");
        setDurationMinutes("");
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }

  return (
    <form className="exercise-form" onSubmit={handleSubmit}>
      <h4>Add Exercise</h4>

      <label className="form-label" htmlFor={`exercise-${workoutId}`}>
        Exercise
      </label>

      <select className="exercise-select"
        id={`exercise-${workoutId}`}
        value={exerciseId}
        onChange={(event) =>
          setExerciseId(event.target.value)
        }
        required
      >
        <option value="">Select an exercise</option>

        {exercises.map((exercise) => (
          <option key={exercise.id} value={exercise.id}>
            {exercise.name}
          </option>
        ))}
      </select>

      {exerciseId && isCardio ? (
        <>
          <label className="form-label" htmlFor={`duration-${workoutId}`}>
            Duration in minutes
          </label>

          <input
            id={`duration-${workoutId}`}
            type="number"
            min="1"
            value={durationMinutes}
            onChange={(event) =>
              setDurationMinutes(event.target.value)
            }
            required
          />
        </>
      ) : exerciseId ? (
        <>
          <label className="form-label" htmlFor={`sets-${workoutId}`}>
            Sets
          </label>

          <input
            id={`sets-${workoutId}`}
            type="number"
            min="1"
            value={sets}
            onChange={(event) =>
              setSets(event.target.value)
            }
            required
          />

          <label className="form-label" htmlFor={`reps-${workoutId}`}>
            Reps
          </label>

          <input
            id={`reps-${workoutId}`}
            type="number"
            min="1"
            value={reps}
            onChange={(event) =>
              setReps(event.target.value)
            }
            required
          />

          <input
            type="number"
            min="0"
            step="0.5"
            placeholder="Weight"
            value={weight}
            onChange={(event) =>
              setWeight(event.target.value)
            }
          />

        </>
      ) : null}

      <button className="form-button"
        type="submit"
        disabled={isLoading || !exerciseId}
      >
        {isLoading ? "Adding..." : "Add Exercise"}
      </button>

      {error && <p className="form-error">{error}</p>}
    </form>
  );
}

export default AddExerciseForm;