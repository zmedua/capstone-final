import WorkoutCard from "../components/WorkoutCard";

function WorkoutHistoryPage({ workouts, setWorkouts }) {
  const completedWorkouts = workouts.filter(
    (workout) => workout.completed
  );

  function handleWorkoutUpdated(updatedWorkout) {
    setWorkouts((currentWorkouts) =>
      currentWorkouts.map((workout) =>
        workout.id === updatedWorkout.id
          ? updatedWorkout
          : workout
      )
    );
  }

  return (
    <main className="history-page">
      <h1>Workout History</h1>

      {completedWorkouts.length === 0 ? (
        <p>No completed workouts yet.</p>
      ) : (
        completedWorkouts.map((workout) => (
          <WorkoutCard
            key={workout.id}
            workout={workout}
            onWorkoutUpdated={handleWorkoutUpdated}
          />
        ))
      )}
    </main>
  );
}

export default WorkoutHistoryPage;