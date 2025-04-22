import React from "react";
import "../styles/MessageBubble.css";

export default function MessageBubble({ sender, text }) {
  return (
    <div className={`message-bubble ${sender}`}>
      <strong>{sender === "user" ? "You" : "Bot"}:</strong> {text}
    </div>
  );
}
