// src/pages/SignupPage.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Cross, Eye, EyeOff } from "lucide-react";

import "../styles/SignupPage.css";

function SignupPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [error, setError] = useState("");
  const [password, setPassword] = useState("");
  const [requirements, setRequirements] = useState({
    letter: false,
    capital: false,
    number: false,
    special: false,
    length: false,
  });

  const handlePasswordChange = (e) => {
    const pwd = e.target.value;
    setPassword(pwd);

    setRequirements({
      letter: /[a-zA-Z]/.test(pwd),
      capital: /[A-Z]/.test(pwd),
      number: /\d/.test(pwd),
      special: /[^a-zA-Z0-9]/.test(pwd),
      length: pwd.length >= 8,
    });
  };

  const baseUrl = process.env.REACT_APP_API_URL;

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${baseUrl}/api/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      });

      if (!response.ok) {
        throw new Error("Signup failed");
      }

      const data = await response.json();
      console.log("Signup successful", data);
      navigate("/");
    } catch (err) {
      setError("Signup failed. Please try again.");
      console.error(err);
    }
  };

  return (
    <div className="signup-container">
      <form onSubmit={handleSignup} className="signup-form">
        <div className="auth-header">
          <Cross className="auth-icon" />
          <h1>CareGPT</h1>
        </div>
        <h2>Sign Up</h2>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <div className="password-input-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={handlePasswordChange}
            required
          />
          <button
            type="button"
            className="toggle-password-btn"
            onClick={() => setShowPassword((prev) => !prev)}
          >
            {showPassword ? (
              <EyeOff size={18} color="#666" />
            ) : (
              <Eye size={18} color="#666" />
            )}
          </button>
        </div>

        <div className="password-checklist">
          <p>Password must meet the following requirements:</p>
          <ul>
            <li style={{ color: requirements.letter ? "green" : "red" }}>
              {requirements.letter ? "✔" : "✖"} At least{" "}
              <strong>one letter</strong>
            </li>
            <li style={{ color: requirements.capital ? "green" : "red" }}>
              {requirements.capital ? "✔" : "✖"} At least{" "}
              <strong>one capital letter</strong>
            </li>
            <li style={{ color: requirements.number ? "green" : "red" }}>
              {requirements.number ? "✔" : "✖"} At least{" "}
              <strong>one number</strong>
            </li>
            <li style={{ color: requirements.special ? "green" : "red" }}>
              {requirements.special ? "✔" : "✖"} Include{" "}
              <strong>one special character</strong>
            </li>
            <li style={{ color: requirements.length ? "green" : "red" }}>
              {requirements.length ? "✔" : "✖"} Be at least{" "}
              <strong>8 characters</strong>
            </li>
          </ul>
        </div>

        {error && <p className="error-text">{error}</p>}
        <button type="submit">Create Account</button>
        <p className="redirect-text">
          Already have an account?{" "}
          <span onClick={() => navigate("/")}>Log In</span>
        </p>
      </form>
    </div>
  );
}

export default SignupPage;
