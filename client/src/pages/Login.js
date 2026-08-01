import React from "react";
import {Link} from "react-router-dom";
import LoginForm from "../components/LoginForm";
import "../styles/Login.css";
function Login({ onLogin }) {
  return (
    <main>
      <h1 className="login-title">Employee Workout Tracker</h1>
      <h2 className="login-prompt">Login</h2>
      <LoginForm onLogin={onLogin} />
      <p className="signup-prompt">
        No Account?{" "}
        <Link to ="/signup">Sign up</Link>
        
      </p>
    </main>
  );
}

export default Login;