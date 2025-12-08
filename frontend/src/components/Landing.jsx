import React from "react";

export default function Landing({ onGetStarted }) {
  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "Arial, sans-serif",
      padding: "20px"
    }}>
      <div style={{ maxWidth: "900px", width: "100%", textAlign: "center", color: "white" }}>
        <h1 style={{ fontSize: "3.5rem", marginBottom: "20px", fontWeight: "bold", textShadow: "2px 2px 4px rgba(0,0,0,0.3)" }}>
          AI Chat Assistant
        </h1>
        <p style={{ fontSize: "1.5rem", marginBottom: "40px", opacity: 0.95, lineHeight: "1.6" }}>
          Your intelligent conversation partner powered by AI.
        </p>

        <div style={{ display: "flex", gap: "20px", justifyContent: "center", marginBottom: "60px", flexWrap: "wrap" }}>
          {["💬 Smart Conversations", "📚 Chat History", "⚡ Fast & Reliable"].map((t, i) => (
            <div key={i} style={{
              backgroundColor: "rgba(255,255,255,0.1)",
              backdropFilter: "blur(10px)",
              padding: "30px",
              borderRadius: "12px",
              maxWidth: "250px",
              border: "1px solid rgba(255,255,255,0.2)"
            }}>
              <div style={{ fontSize: "2.5rem", marginBottom: "15px" }}>{t.split(" ")[0]}</div>
              <h3 style={{ fontSize: "1.2rem", marginBottom: "10px" }}>{t.split(" ")[1]}</h3>
              <p style={{ fontSize: "0.9rem", opacity: 0.9 }}>Description goes here</p>
            </div>
          ))}
        </div>

        <button
          onClick={onGetStarted}
          style={{
            padding: "18px 50px",
            fontSize: "1.2rem",
            fontWeight: "bold",
            backgroundColor: "white",
            color: "#667eea",
            border: "none",
            borderRadius: "50px",
            cursor: "pointer",
            boxShadow: "0 4px 15px rgba(0,0,0,0.2)"
          }}>
          Get Started
        </button>

        <p style={{ marginTop: "30px", fontSize: "0.9rem", opacity: 0.8 }}>Free to use • No credit card required</p>
      </div>
    </div>
  );
}
