// import React, { useEffect, useRef, useState } from "react";
// import MessageBubble from "./MessageBubble";
// import { fetchChatMessages, postMessage, createChat, fetchChats } from "../api";

// export default function ChatArea({
//   apiBase,
//   token,
//   currentChatId,
//   setCurrentChatId,
//   chats,
//   setChats,
//   sidebarOpen,
//   setSidebarOpen
// }) {
//   const [history, setHistory] = useState([]);
//   const [text, setText] = useState("");
//   const boxRef = useRef();

//   useEffect(() => {
//     if (currentChatId) loadChatMessages(currentChatId);
//     else setHistory([]);
//     // eslint-disable-next-line
//   }, [currentChatId, token]);

//   useEffect(() => {
//     if (boxRef.current) boxRef.current.scrollTop = boxRef.current.scrollHeight;
//   }, [history]);

//   const loadChatMessages = async (chatId) => {
//     try {
//       const data = await fetchChatMessages(apiBase, token, chatId);
//       setHistory(data);
//     } catch (err) {
//       console.error("loadChatMessages:", err);
//     }
//   };

//   const createNewChat = async () => {
//     try {
//       const newChat = await createChat(apiBase, token);
//       setChats([newChat, ...chats]);
//       setCurrentChatId(newChat.id);
//       setHistory([]);
//     } catch (err) {
//       console.error(err);
//       alert("Error creating chat");
//     }
//   };

//   const send = async () => {
//     if (!text.trim()) return;

//     let chatId = currentChatId;
//     if (!chatId) {
//       try {
//         const newChat = await createChat(apiBase, token);
//         chatId = newChat.id;
//         setCurrentChatId(chatId);
//         setChats([newChat, ...chats]);
//       } catch (err) {
//         alert("Error creating chat: " + err.message);
//         return;
//       }
//     }

//     const userTemp = { id: "temp-" + Date.now(), role: "user", text, timestamp: new Date().toISOString() };
//     setHistory(h => [...h, userTemp]);
//     setText("");

//     try {
//       const data = await postMessage(apiBase, token, userTemp.text, chatId);
//       setHistory(h => [...h.filter(m => m.id !== userTemp.id), data.user, data.ai]);
//       // refresh chats & counts
//       const fresh = await fetchChats(apiBase, token);
//       setChats(fresh);
//     } catch (err) {
//       console.error("Error sending message:", err);
//       setHistory(h => [
//         ...h.filter(m => m.id !== userTemp.id),
//         { id: "err-" + Date.now(), role: "ai", text: `Error: ${err.message}`, timestamp: new Date().toISOString() }
//       ]);
//     }
//   };

//   return (
//     <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
//       {!sidebarOpen && (
//         <button onClick={() => setSidebarOpen(true)} style={{
//           position: "absolute", left: 10, top: 10, padding: "8px 12px",
//           backgroundColor: "#2196F3", color: "white", border: "none", borderRadius: 4, cursor: "pointer"
//         }}>
//           ☰ Chats
//         </button>
//       )}

//       <div style={{ flex: 1, display: "flex", flexDirection: "column", maxWidth: "900px", margin: "0 auto", width: "100%", padding: 20 }}>
//         <div style={{ marginBottom: 12 }}>
//           <h2 style={{ margin: 0 }}>AI Chat</h2>
//           {currentChatId && chats.find(c => c.id === currentChatId) && (
//             <div style={{ fontSize: 14, color: "#666", marginTop: 4 }}>{chats.find(c => c.id === currentChatId)?.title}</div>
//           )}
//         </div>

//         <div ref={boxRef} style={{ flex: 1, overflowY: "auto", border: "1px solid #eee", padding: 12, borderRadius: 8, backgroundColor: "#fafafa", minHeight: 0 }}>
//           {history.length === 0 ? (
//             <div style={{ textAlign: "center", color: "#999", marginTop: 40 }}>Start a conversation by typing a message below</div>
//           ) : (
//             history.map(m => <MessageBubble key={m.id} m={m} />)
//           )}
//         </div>

//         <div style={{ display: "flex", marginTop: 12 }}>
//           <input
//             value={text}
//             onChange={e => setText(e.target.value)}
//             onKeyDown={e => e.key === "Enter" && !e.shiftKey && send()}
//             style={{ flex: 1, padding: 12, borderRadius: 8, border: "1px solid #ddd", fontSize: 14 }}
//             placeholder="Type a message..."
//           />
//           <button onClick={send} style={{ marginLeft: 8, padding: "12px 24px", backgroundColor: "#2196F3", color: "white", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: "bold" }}>
//             Send
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }


import React, { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";
import { fetchChatMessages, postMessage, createChat, fetchChats } from "../api";

export default function ChatArea({
  apiBase,
  token,
  currentChatId,
  setCurrentChatId,
  chats,
  setChats,
  sidebarOpen,
  setSidebarOpen
}) {
  const [history, setHistory] = useState([]);
  const [text, setText] = useState("");
  const [isSending, setIsSending] = useState(false);
  const boxRef = useRef();

  // load messages when chat changes, but skip while sending (prevents race on first chat)
  useEffect(() => {
    if (!token) return;
    if (!currentChatId) {
      setHistory([]);
      return;
    }
    if (isSending) return; // don't load messages while a send is in-flight
    loadChatMessages(currentChatId);
    // eslint-disable-next-line
  }, [currentChatId, token, isSending]);

  useEffect(() => {
    if (boxRef.current) boxRef.current.scrollTop = boxRef.current.scrollHeight;
  }, [history]);

  const loadChatMessages = async (chatId) => {
    try {
      const data = await fetchChatMessages(apiBase, token, chatId);
      setHistory(data);
    } catch (err) {
      console.error("loadChatMessages:", err);
    }
  };

  const createNewChat = async () => {
    try {
      const newChat = await createChat(apiBase, token);
      setChats([newChat, ...chats]);
      setCurrentChatId(newChat.id);
      setHistory([]);
    } catch (err) {
      console.error(err);
      alert("Error creating chat");
    }
  };

  const send = async () => {
    if (!text.trim()) return;
    if (isSending) return; // guard against double submits
    setIsSending(true);

    try {
      // 1) Ensure chat exists (create and await)
      let chatId = currentChatId;
      if (!chatId) {
        const newChat = await createChat(apiBase, token);
        chatId = newChat.id;
        setCurrentChatId(chatId);
        setChats(prev => [newChat, ...prev]);
        // Clear any stale history to avoid merging old local UI with server results
        setHistory([]);
      }

      // 2) Optimistic UI: add temp user message
      const userTemp = { id: "temp-" + Date.now(), role: "user", text, timestamp: new Date().toISOString() };
      setHistory(h => [...h, userTemp]);
      setText("");

      // 3) Post message (server inserts user + ai)
      const data = await postMessage(apiBase, token, userTemp.text, chatId);

      // 4) Replace temp message and append server-saved messages (user + ai)
      setHistory(h => {
        const filtered = h.filter(m => m.id !== userTemp.id);
        return [...filtered, data.user, data.ai];
      });

      // 5) Refresh chats to update counts/titles
      const fresh = await fetchChats(apiBase, token);
      setChats(fresh);
    } catch (err) {
      console.error("Error sending message:", err);
      // remove temp and show error message bubble
      setHistory(h => [
        ...h.filter(m => !String(m.id).startsWith("temp-")),
        { id: "err-" + Date.now(), role: "ai", text: `Error: ${err.message}`, timestamp: new Date().toISOString() }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  // Defensive dedupe for rendering (keyed by id or fallback composite)
  const dedupedHistory = (() => {
    const map = new Map();
    for (const m of history) {
      const key = m.id ?? `${m.role}-${m.text}-${m.timestamp}`;
      if (!map.has(key)) map.set(key, m);
    }
    return Array.from(map.values());
  })();

  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
      {!sidebarOpen && (
        <button onClick={() => setSidebarOpen(true)} style={{
          position: "absolute", left: 10, top: 10, padding: "8px 12px",
          backgroundColor: "#2196F3", color: "white", border: "none", borderRadius: 4, cursor: "pointer"
        }}>
          ☰ Chats
        </button>
      )}

      <div style={{ flex: 1, display: "flex", flexDirection: "column", maxWidth: "900px", margin: "0 auto", width: "100%", padding: 20 }}>
        <div style={{ marginBottom: 12 }}>
          <h2 style={{ margin: 0 }}>AI Chat</h2>
          {currentChatId && chats.find(c => c.id === currentChatId) && (
            <div style={{ fontSize: 14, color: "#666", marginTop: 4 }}>{chats.find(c => c.id === currentChatId)?.title}</div>
          )}
        </div>

        <div ref={boxRef} style={{ flex: 1, overflowY: "auto", border: "1px solid #eee", padding: 12, borderRadius: 8, backgroundColor: "#fafafa", minHeight: 0 }}>
          {dedupedHistory.length === 0 ? (
            <div style={{ textAlign: "center", color: "#999", marginTop: 40 }}>Start a conversation by typing a message below</div>
          ) : (
            dedupedHistory.map(m => <MessageBubble key={m.id ?? `${m.role}-${m.timestamp}`} m={m} />)
          )}
        </div>

        <div style={{ display: "flex", marginTop: 12 }}>
          <input
            value={text}
            onChange={e => setText(e.target.value)}
            onKeyDown={e => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault(); // avoid form submit / duplicate event
                send();
              }
            }}
            disabled={isSending}
            style={{ flex: 1, padding: 12, borderRadius: 8, border: "1px solid #ddd", fontSize: 14, opacity: isSending ? 0.8 : 1 }}
            placeholder={isSending ? "Sending..." : "Type a message..."}
          />
          <button
            onClick={send}
            disabled={isSending}
            style={{
              marginLeft: 8,
              padding: "12px 24px",
              backgroundColor: isSending ? "#6fa8ff" : "#2196F3",
              color: "white",
              border: "none",
              borderRadius: 8,
              cursor: isSending ? "not-allowed" : "pointer",
              fontWeight: "bold"
            }}
          >
            {isSending ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
