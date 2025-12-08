import React from "react";

export default function ChatListItem({ chat, active, onClick, onDelete }) {
  return (
    <div
      onClick={onClick}
      style={{
        padding: "12px",
        marginBottom: "4px",
        borderRadius: "8px",
        cursor: "pointer",
        backgroundColor: active ? "#e3f2fd" : "transparent",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
      }}
      onMouseEnter={(e) => { if (!active) e.currentTarget.style.backgroundColor = "#eeeeee"; }}
      onMouseLeave={(e) => { if (!active) e.currentTarget.style.backgroundColor = "transparent"; }}
    >
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontWeight: active ? "bold" : "normal", fontSize: 14, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {chat.title}
        </div>
        <div style={{ fontSize: 11, color: "#666", marginTop: 4 }}>{chat.message_count} messages</div>
      </div>
      <button onClick={onDelete} style={{ background: "none", border: "none", color: "#f44336", cursor: "pointer", padding: "4px 8px", fontSize: 18, opacity: 0.7 }} title="Delete chat">×</button>
    </div>
  );
}
