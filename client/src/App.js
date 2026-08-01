import React, { useEffect, useState } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import NavBar from "./components/NavBar";
import Login from "./pages/Login";
import WorkoutsPage from "./pages/WorkoutsPage";
import AddWorkoutPage from "./pages/AddWorkoutPage";
import WorkoutHistoryPage from "./pages/WorkoutHistoryPage";
import ExercisesPage from "./pages/ExercisesPage";
import FavoritesPage from "./pages/FavoritesPage";
import Signup from "./pages/Signup";

import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const [workouts, setWorkouts] = useState([]);
  const [exercises, setExercises] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [appError, setAppError] = useState("");

  // Check whether the user already has an active session.
  useEffect(() => {
    fetch("/check_session")
      .then((response) => {
        if (!response.ok) {
          return null;
        }

        return response.json();
      })
      .then((userData) => {
        setUser(userData);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Session check failed:", error);
        setUser(null);
        setIsLoading(false);
      });
  }, []);

  // Load application data after login.
  useEffect(() => {
    if (!user) {
      setWorkouts([]);
      setExercises([]);
      setFavorites([]);
      return;
    }

    setAppError("");

    Promise.all([
      fetch("/workouts"),
      fetch("/exercises"),
      fetch("/favorites"),
    ])
      .then(async ([workoutResponse, exerciseResponse, favoriteResponse]) => {
        if (
          !workoutResponse.ok ||
          !exerciseResponse.ok ||
          !favoriteResponse.ok
        ) {
          throw new Error("Unable to load application data.");
        }

        const workoutData = await workoutResponse.json();
        const exerciseData = await exerciseResponse.json();
        const favoriteData = await favoriteResponse.json();

        return {
          workoutData,
          exerciseData,
          favoriteData,
        };
      })
      .then(({ workoutData, exerciseData, favoriteData }) => {
        setWorkouts(workoutData.workouts || workoutData);
        setExercises(exerciseData.exercises || exerciseData);
        setFavorites(favoriteData.favorites || favoriteData);
      })
      .catch((error) => {
        console.error(error);
        setAppError(error.message);
      });
  }, [user]);

  function handleLogin(userData) {
    setUser(userData);
  }

  function handleLogout() {
    fetch("/logout", {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Unable to log out.");
        }

        setUser(null);
        setWorkouts([]);
        setExercises([]);
        setFavorites([]);
        setAppError("");
      })
      .catch((error) => {
        console.error(error);
        setAppError(error.message);
      });
  }

  function handleAddWorkout(newWorkout) {
    setWorkouts((currentWorkouts) => [
      ...currentWorkouts,
      newWorkout,
    ]);
  }

  function handleWorkoutUpdated(updatedWorkout) {
    setWorkouts((currentWorkouts) =>
      currentWorkouts.map((workout) =>
        workout.id === updatedWorkout.id
          ? updatedWorkout
          : workout
      )
    );
  }

  function handleWorkoutDeleted(workoutId) {
    setWorkouts((currentWorkouts) =>
      currentWorkouts.filter(
        (workout) => workout.id !== workoutId
      )
    );
  }

  if (isLoading) {
    return <p>Loading...</p>;
  }

  return (
    <BrowserRouter>
      {user && (
        <NavBar
          user={user}
          onLogout={handleLogout}
        />
      )}

      {appError && (
        <p className="error-message">
          {appError}
        </p>
      )}

      <Routes>
        <Route
          path="/login"
          element={
            user ? (
              <Navigate to="/workouts" replace />
            ) : (
              <Login onLogin={handleLogin} />
            )
          }
        />

        <Route
          path="/signup"
          element={
            user ? (
              <Navigate to="/workouts" replace />
            ) : (
              <Signup onSignup={handleLogin} />
            )
          }
        />

        <Route
          path="/workouts"
          element={
            user ? (
              <WorkoutsPage
                workouts={workouts}
                setWorkouts={setWorkouts}
                exercises={exercises}
                onWorkoutUpdated={handleWorkoutUpdated}
                onWorkoutDeleted={handleWorkoutDeleted}
              />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="/workouts/new"
          element={
            user ? (
              <AddWorkoutPage
                onAddWorkout={handleAddWorkout}
              />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="/history"
          element={
            user ? (
              <WorkoutHistoryPage
                workouts={workouts}
                onWorkoutUpdated={handleWorkoutUpdated}
                onWorkoutDeleted={handleWorkoutDeleted}
              />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="/exercises"
          element={
            user ? (
              <ExercisesPage
                exercises={exercises}
                favorites={favorites}
                setFavorites={setFavorites}
              />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="/favorites"
          element={
            user ? (
              <FavoritesPage
                favorites={favorites}
                setFavorites={setFavorites}
              />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="*"
          element={
            <Navigate
              to={user ? "/workouts" : "/login"}
              replace
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;