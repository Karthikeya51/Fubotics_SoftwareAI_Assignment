import React from "react";
import ChatListItem from "./ChatListItem";

export default function ChatList({ chats, currentChatId, onSelect, onDelete }) {
  return (
    <>
      {chats.map(chat => (
        <ChatListItem
          key={chat.id}
          chat={chat}
          active={currentChatId === chat.id}
          onClick={() => onSelect(chat.id)}
          onDelete={(e) => onDelete(chat.id, e)}
        />
      ))}
    </>
  );
}
