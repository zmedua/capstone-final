import ExerciseCard from "../components/ExerciseCard";
import "../styles/ExerciseCard.css";
function FavoritesPage({
  favorites,
  setFavorites,
}) {
  return (
    <main className="favorites-page">
      <h1>Favorite Exercises</h1>

      {favorites.length === 0 ? (
        <p>You have not saved any favorites.</p>
      ) : (
        <section className="exercise-grid">
          {favorites.map((favorite) => (
            <ExerciseCard
              key={favorite.id}
              exercise={favorite.exercise}
              isFavorite={true}
              setFavorites={setFavorites}
            />
          ))}
        </section>
      )}
    </main>
  );
}

export default FavoritesPage;