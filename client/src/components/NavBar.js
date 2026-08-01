import React from "react";
import {NavLink, useNavigate,} from "react-router-dom";
import "../styles/NavBar.css";

function NavBar({ user, onLogout }) 
{ const navigate = useNavigate();

  function handleLogoutClick(){
    onLogout();
    navigate("/login");
  }
  return (
    <nav className="navbar">
      
      <h1 className="navbar-title">Workout Tracker</h1>
      <p className="navbar-welcome">Welcome, {user.username}</p>

      <NavLink to="/workouts">
        Workouts
      </NavLink>

      {"|"}

      <NavLink to="/workouts/new">
        Add Workout
      </NavLink>

      {"|"}

      <NavLink to="/history">
        History
      </NavLink>

      {"|"}

      <NavLink to="/exercises">
        Exercises
      </NavLink>

      {"|"}

      <NavLink to="/favorites">
        Favorites
      </NavLink>
      
      {"|"}

      <button className="nav-button" type="button" onClick={handleLogoutClick}>
        Logout
      </button>
    </nav>
  );
}

export default NavBar;