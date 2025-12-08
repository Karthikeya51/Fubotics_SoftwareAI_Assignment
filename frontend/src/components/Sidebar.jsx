import React from "react";
import ChatList from "./ChatList";
import { createChat, deleteChatApi } from "../api";

export default function Sidebar({
  chats,
  setChats,
  currentChatId,
  setCurrentChatId,
  sidebarOpen,
  setSidebarOpen,
  loadChats,
  currentUser,
  onLogout,
  apiBase,
  token
}) {
  const createNewChat = async () => {
    try {
      const newChat = await createChat(apiBase, token);
      setChats([newChat, ...chats]);
      setCurrentChatId(newChat.id);
    } catch (err) {
      console.error("createNewChat:", err);
      alert("Error creating chat");
    }
  };

  const deleteChat = async (chatId, e) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this chat?")) return;
    try {
      await deleteChatApi(apiBase, token, chatId);
      const remaining = chats.filter(c => c.id !== chatId);
      setChats(remaining);
      if (currentChatId === chatId) {
        if (remaining.length > 0) setCurrentChatId(remaining[0].id);
        else setCurrentChatId(null);
      }
    } catch (err) {
      console.error("deleteChat:", err);
      alert("Error deleting chat");
    }
  };

  return (
    <div style={{
      width: sidebarOpen ? "260px" : "0",
      overflow: "hidden",
      backgroundColor: "#f5f5f5",
      borderRight: "1px solid #ddd",
      display: "flex",
      flexDirection: "column",
      transition: "width 0.3s"
    }}>
      <div style={{ padding: "16px", borderBottom: "1px solid #ddd" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <h3 style={{ margin: 0, fontSize: 18 }}>Chats</h3>
          <button onClick={() => setSidebarOpen(false)} style={{ background: "none", border: "none", cursor: "pointer", fontSize: 20 }}>×</button>
        </div>
        <button onClick={createNewChat} style={{
          width: "100%",
          padding: "10px",
          backgroundColor: "#2196F3",
          color: "white",
          border: "none",
          borderRadius: 4,
          cursor: "pointer",
          fontWeight: "bold"
        }}>
          + New Chat
        </button>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "8px" }}>
        <ChatList chats={chats} currentChatId={currentChatId} onSelect={setCurrentChatId} onDelete={deleteChat} />
        {chats.length === 0 && <div style={{ padding: 20, textAlign: "center", color: "#999" }}>No chats yet. Create a new chat to get started!</div>}
      </div>

      <div style={{ padding: "12px", borderTop: "1px solid #ddd" }}>
        <div style={{ fontSize: 12, color: "#666", marginBottom: 8 }}>Welcome, {currentUser?.username}</div>
        <button onClick={onLogout} style={{
          width: "100%",
          padding: "8px",
          backgroundColor: "#f44336",
          color: "white",
          border: "none",
          borderRadius: 4,
          cursor: "pointer"
        }}>
          Logout
        </button>
      </div>
    </div>
  );
}
