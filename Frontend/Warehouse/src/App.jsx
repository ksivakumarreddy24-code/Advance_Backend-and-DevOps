
import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import "./App.css";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [token, setToken] = useState("");
  const [showLogin, setShowLogin] = useState(true);
  const [message, setMessage] = useState("");

  // User login
  function login(username, password) {
    fetch(API_URL + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username,
        password: password
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          setMessage(data.detail);
        } else {
          setToken(data.access_token);
          setMessage("Login successful");
        }
      });
  }

  // User registration
  function register(username, password) {
    fetch(API_URL + "/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username,
        password: password
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          setMessage(data.detail);
        } else {
          setMessage("Registration successful. Please login.");
          setShowLogin(true);
        }
      });
  }

  // Logout
  function logout() {
    setToken("");
    setMessage("");
  }

  // Login 
  if (token === "") {
    return (
      <div className="page">
        <div className="auth-box">

          <h1>Warehouse Dispatch</h1>
          <p>{message}</p>

          {showLogin ? (
            <Login
              onLogin={login}
              onRegister={() => {
                setShowLogin(false);
                setMessage("");
              }}
            />
          ) : (
            <Register
              onRegister={register}
              onLogin={() => {
                setShowLogin(true);
                setMessage("");
              }}
            />
          )}

        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="auth-box">
        <h1>Welcome to Warehouse Dispatch</h1>
        <p>Login successful!</p>
        <button onClick={logout}>Log out</button>
      </div>
    </div>
  );
}

export default App;
