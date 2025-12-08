import React from "react";

export default function MessageBubble({ m }) {
  return (
    <div style={{ margin: "8px 0", textAlign: m.role === "user" ? "right" : "left" }}>
      <div style={{ display: "inline-block", padding: 10, borderRadius: 8, background: m.role === "user" ? "#d1f0ff" : "#f0f0f0", maxWidth: "80%" }}>
        <small style={{ opacity: 0.8, textTransform: "uppercase" }}>{m.role}</small>
        <div style={{ marginTop: 6, whiteSpace: "pre-wrap" }}>{m.text}</div>
        <div style={{ fontSize: 10, opacity: 0.7, marginTop: 6 }}>{new Date(m.timestamp).toLocaleString()}</div>
      </div>
    </div>
  );
}
