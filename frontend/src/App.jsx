
import React, { useEffect, useState } from "react";
import Landing from "./components/Landing";
import Auth from "./components/Auth";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import { getMe, fetchChats } from "./api";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLanding, setShowLanding] = useState(true);
  const [showLogin, setShowLogin] = useState(true);
  const [currentUser, setCurrentUser] = useState(null);
  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const API = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/+$/, "");
  const url = (p) => new URL(p, API + "/").toString(); // url("/register")


  useEffect(() => {
    if (token) {
      checkAuth();
      loadChats();
      setShowLanding(false);
    } else {
      setShowLanding(true);
    }
    // eslint-disable-next-line
  }, [token]);

  const checkAuth = async () => {
    try {
      const user = await getMe(API, token);
      setCurrentUser(user);
      setIsAuthenticated(true);
    } catch (err) {
      localStorage.removeItem("token");
      setToken("");
      setIsAuthenticated(false);
    }
  };

  const loadChats = async () => {
    try {
      const data = await fetchChats(API, token);
      setChats(data);
      if (data.length > 0 && !currentChatId) {
        setCurrentChatId(data[0].id);
      }
    } catch (err) {
      console.error("loadChats:", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
    setIsAuthenticated(false);
    setCurrentUser(null);
    setChats([]);
    setCurrentChatId(null);
  };

  // When user successfully logs in (child component -> parent)
  const onLogin = (accessToken) => {
    setToken(accessToken);
    localStorage.setItem("token", accessToken);
    setIsAuthenticated(true);
  };

  if (!isAuthenticated && showLanding) {
    return <Landing onGetStarted={() => setShowLanding(false)} />;
  }

  if (!isAuthenticated && !showLanding) {
    return (
      <Auth
        apiBase={API}
        showLogin={showLogin}
        setShowLogin={setShowLogin}
        onLogin={onLogin}
        onBack={() => setShowLanding(true)}
      />
    );
  }

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      <Sidebar
        chats={chats}
        setChats={setChats}
        currentChatId={currentChatId}
        setCurrentChatId={setCurrentChatId}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        loadChats={loadChats}
        currentUser={currentUser}
        onLogout={handleLogout}
        apiBase={API}
        token={token}
      />
      <ChatArea
        apiBase={API}
        token={token}
        currentChatId={currentChatId}
        setCurrentChatId={setCurrentChatId}
        chats={chats}
        setChats={setChats}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />
    </div>
  );
}
