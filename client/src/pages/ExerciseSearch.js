function ExerciseSearch({
  searchTerm,
  setSearchTerm,
  categoryFilter,
  setCategoryFilter,
  difficultyFilter,
  setDifficultyFilter,
}) {
  return (
    <section className="exercise-search">
      <input
        type="text"
        placeholder="Search exercises"
        value={searchTerm}
        onChange={(event) =>
          setSearchTerm(event.target.value)
        }
      />

      <select
        value={categoryFilter}
        onChange={(event) =>
          setCategoryFilter(event.target.value)
        }
      >
        <option value="all">All Categories</option>
        <option value="Strength">Strength</option>
        <option value="Cardio">Cardio</option>
        <option value="Flexibility">Flexibility</option>
      </select>

      <select
        value={difficultyFilter}
        onChange={(event) =>
          setDifficultyFilter(event.target.value)
        }
      >
        <option value="all">All Difficulties</option>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
    </section>
  );
}

export default ExerciseSearch;