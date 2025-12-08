import React, { useState } from "react";
import { loginApi, registerApi } from "../api";

export default function Auth({ apiBase, showLogin, setShowLogin, onLogin, onBack }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const data = await loginApi(apiBase, username, password);
      onLogin(data.access_token);
      setUsername("");
      setPassword("");
    } catch (err) {
      alert(err.message || "Login failed");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await registerApi(apiBase, username, email, password);
      alert("Registration successful! Please login.");
      setShowLogin(true);
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (err) {
      alert(err.message || "Registration failed");
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      padding: "20px"
    }}>
      <div style={{
        maxWidth: 400,
        width: "100%",
        backgroundColor: "white",
        padding: "40px",
        borderRadius: "16px",
        boxShadow: "0 10px 40px rgba(0,0,0,0.2)"
      }}>
        <div style={{ marginBottom: "20px", textAlign: "center" }}>
          <h2 style={{ margin: "0 0 10px 0", color: "#333", fontSize: "1.8rem" }}>
            {showLogin ? "Welcome Back" : "Create Account"}
          </h2>
          <p style={{ color: "#666", fontSize: "0.9rem" }}>
            {showLogin ? "Sign in to continue" : "Start your AI chat journey"}
          </p>
        </div>

        {showLogin ? (
          <form onSubmit={handleLogin}>
            <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="Username" required style={inputStyle} />
            <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" type="password" required style={inputStyle} />
            <button type="submit" style={primaryBtn}>Login</button>
            <div style={{textAlign:"center"}}>
              <button type="button" onClick={() => setShowLogin(false)} style={linkBtn}>Don't have an account? Register</button>
            </div>
            <div style={{textAlign:"center", marginTop: "15px"}}>
              <button type="button" onClick={onBack} style={ghostBtn}>← Back to Home</button>
            </div>
          </form>
        ) : (
          <form onSubmit={handleRegister}>
            <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="Username" required style={inputStyle} />
            <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" type="email" required style={inputStyle} />
            <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" type="password" required style={inputStyle} />
            <button type="submit" style={primaryBtn}>Register</button>
            <div style={{textAlign:"center"}}>
              <button type="button" onClick={() => setShowLogin(true)} style={linkBtn}>Already have an account? Login</button>
            </div>
            <div style={{textAlign:"center", marginTop: "15px"}}>
              <button type="button" onClick={onBack} style={ghostBtn}>← Back to Home</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "12px",
  boxSizing: "border-box",
  border: "1px solid #ddd",
  borderRadius: "8px",
  fontSize: "1rem",
  marginBottom: 12
};

const primaryBtn = {
  width: "100%",
  padding: "14px",
  marginBottom: 16,
  backgroundColor: "#667eea",
  color: "white",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
  fontSize: "1rem",
  fontWeight: "bold"
};

const linkBtn = {
  background: "none",
  border: "none",
  color: "#667eea",
  cursor: "pointer",
  textDecoration: "underline",
  fontSize: "0.9rem"
};

const ghostBtn = {
  background: "none",
  border: "none",
  color: "#999",
  cursor: "pointer",
  fontSize: "0.85rem"
};
