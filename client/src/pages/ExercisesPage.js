import { useState } from "react";

import ExerciseSearch from "./ExerciseSearch";
import ExerciseCard from "../components/ExerciseCard";

function ExercisesPage({
  exercises,
  favorites,
  setFavorites,
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const [categoryFilter, setCategoryFilter] =
    useState("all");
  const [difficultyFilter, setDifficultyFilter] =
    useState("all");

  const favoriteExerciseIds = favorites.map(
    (favorite) => favorite.exercise.id
  );

  const filteredExercises = exercises.filter((exercise) => {
    const matchesSearch = exercise.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());

    const matchesCategory =
      categoryFilter === "all" ||
      exercise.category === categoryFilter;

    const matchesDifficulty =
      difficultyFilter === "all" ||
      exercise.difficulty === difficultyFilter;

    return (
      matchesSearch &&
      matchesCategory &&
      matchesDifficulty
    );
  });

  return (
    <main className="exercises-page">
      <h1>Exercises</h1>

      <ExerciseSearch
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        categoryFilter={categoryFilter}
        setCategoryFilter={setCategoryFilter}
        difficultyFilter={difficultyFilter}
        setDifficultyFilter={setDifficultyFilter}
      />

      <section className="exercise-grid">
        {filteredExercises.map((exercise) => (
          <ExerciseCard
            key={exercise.id}
            exercise={exercise}
            isFavorite={favoriteExerciseIds.includes(
              exercise.id
            )}
            setFavorites={setFavorites}
          />
        ))}
      </section>
    </main>
  );
}

export default ExercisesPage;