import { useState } from "react";

function ExerciseCard({
  exercise,
  isFavorite,
  setFavorites,
}) {
  const [error, setError] = useState("");

  function handleAddFavorite() {
    fetch(`/favorites/${exercise.id}`, {
      method: "POST",
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(
              data.error || "Unable to add favorite."
            );
          });
        }

        return response.json();
      })
      .then((newFavorite) => {
        setFavorites((currentFavorites) => [
          ...currentFavorites,
          newFavorite,
        ]);
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  function handleRemoveFavorite() {
    fetch(`/favorites/${exercise.id}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            "Unable to remove favorite."
          );
        }

        setFavorites((currentFavorites) =>
          currentFavorites.filter(
            (favorite) =>
              favorite.exercise.id !== exercise.id
          )
        );
      })
      .catch((error) => {
        setError(error.message);
      });
  }

  return (
    <article className="exercise-card">
      {exercise.image_url && (
        <img
          src={exercise.image_url}
          alt={exercise.name}
        />
      )}

      <h3>{exercise.name}</h3>

      <p>Category: {exercise.category}</p>

      {exercise.muscle_group && (
        <p>Muscle group: {exercise.muscle_group}</p>
      )}

      {exercise.equipment && (
        <p>Equipment: {exercise.equipment}</p>
      )}

      {exercise.difficulty && (
        <p>Difficulty: {exercise.difficulty}</p>
      )}

      {isFavorite ? (
        <button onClick={handleRemoveFavorite}>
          Remove Favorite
        </button>
      ) : (
        <button onClick={handleAddFavorite}>
          Add Favorite
        </button>
      )}

      {error && <p className="error-message">{error}</p>}
    </article>
  );
}

export default ExerciseCard;