// src/pages/LoginPage.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Cross } from "lucide-react";

import "../styles/LoginPage.css";

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const baseURL =
    process.env.REACT_APP_API_URL ||
    `${window.location.protocol}//${window.location.hostname}:8000`;

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${baseURL}/api/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("name", data.name);
      localStorage.setItem("user_id", data.user_id);
      console.log("Successful login");
      navigate("/chat");
    } catch (err) {
      setError("Invalid email or password. Please try again.");
    }
  };

  const goToSignup = () => navigate("/signup");

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <div className="auth-header">
          <Cross className="auth-icon" />
          <h1>CareGPT</h1>
        </div>
        <h2>Login</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="error-text">{error}</p>}
        <button type="submit">Sign In</button>
        <p className="redirect-text">
          Don't have an account? <span onClick={goToSignup}>Sign Up</span>
        </p>
      </form>
    </div>
  );
}

export default LoginPage;
