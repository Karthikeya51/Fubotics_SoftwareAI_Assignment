// api.js
export const getMe = async (API, token) => {
    const resp = await fetch(API + "/me", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!resp.ok) throw new Error("Not authenticated");
    return resp.json();
  };
  
  export const fetchChats = async (API, token) => {
    const resp = await fetch(API + "/chats", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!resp.ok) throw new Error("Failed to fetch chats");
    return resp.json();
  };
  
  export const fetchChatMessages = async (API, token, chatId) => {
    const resp = await fetch(API + `/chats/${chatId}/messages`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!resp.ok) throw new Error("Failed to fetch messages");
    return resp.json();
  };
  
  export const createChat = async (API, token, payload = { title: "New Chat" }) => {
    const resp = await fetch(API + "/chats", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    });
    if (!resp.ok) throw new Error("Failed to create chat");
    return resp.json();
  };
  
  export const deleteChatApi = async (API, token, chatId) => {
    const resp = await fetch(API + `/chats/${chatId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!resp.ok) throw new Error("Failed to delete chat");
    return resp.json();
  };
  
  export const postMessage = async (API, token, text, chat_id) => {
    const resp = await fetch(API + "/message", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ text, chat_id }),
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: `Error ${resp.status}` }));
      throw new Error(err.detail || "Failed to send message");
    }
    return resp.json();
  };
  
  export const loginApi = async (API, username, password) => {
    const resp = await fetch(API + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: "Login failed" }));
      throw new Error(err.detail || "Login failed");
    }
    return resp.json();
  };
  
  export const registerApi = async (API, username, email, password) => {
    const resp = await fetch(API + "/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: "Registration failed" }));
      throw new Error(err.detail || "Registration failed");
    }
    return resp.json();
  };
  