import React from "react";
import "../styles/Sidebar.css";
import { Trash2, MessageCircle } from "lucide-react";

export default function Sidebar({
  chatSessions,
  onSelectSession,
  onNewChat,
  selectedSessionId,
  onDeleteSession,
}) {
  return (
    <div className="sidebar">
      <h3>Chats</h3>
      <button className="new-chat-btn" onClick={onNewChat}>
        + New Chat
      </button>
      <ul className="chat-list">
        {chatSessions.map((session) => (
          <li
            key={session._id}
            className={`chat-item ${
              session._id === selectedSessionId ? "active" : ""
            }`}
          >
            <span
              className="chat-label"
              onClick={() => onSelectSession(session._id)}
            >
              <MessageCircle className="chat-icon" fill="currentColor" />
              {session.title}
            </span>
            <div className="chat-actions">
              <button className="dots-btn">⋮</button>
              <div className="dropdown">
                <button
                  className="delete-btn"
                  onClick={() => onDeleteSession(session._id)}
                >
                  <Trash2 size={16} style={{ marginRight: "6px" }} />
                  Delete
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
