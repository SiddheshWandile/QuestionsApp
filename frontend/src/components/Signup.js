import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Login.css"; 

const Signup = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/api/signup", {
        username,
        password,
      });

      if (response.status === 201) {
        setSuccess("Registration successful! Please log in.");
        setError("");
        setUsername("");
        setPassword("");
        setConfirmPassword("");

        // Redirect to the login page
        navigate("/login");
      }
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError("Username already exists. Please choose another.");
      } else {
        setError("An error occurred. Please try again later.");
      }
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 form">
          <div className="view">
          <h2>Sign Up</h2>
          {error && <div className="alert alert-danger">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}
          <form onSubmit={handleSignup}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                className="form-control"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                className="form-control"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary mt-3">
              Sign Up
            </button>
            <p className="mt-3">
              Already have an account?{" "}
              <a href="/login" onClick={() => navigate("/login")}>
                Log in
              </a>
            </p>
          </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
