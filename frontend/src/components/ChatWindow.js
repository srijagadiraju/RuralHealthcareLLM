// src/components/ChatWindow.js
import React from "react";
import { Cross } from "lucide-react";

import "../styles/ChatWindow.css";

export default function ChatWindow({ messages }) {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`message-bubble ${msg.sender === "user" ? "user" : "bot"}`}
        >
          {msg.sender === "user" ? (
            <strong>You:</strong>
          ) : (
            <strong>
              <Cross style={{ marginRight: "6px" }} size={16} color="#0077cc" />
              Dr. CareGPT:
            </strong>
          )}{" "}
          {msg.text}
          {/* Show disclaimer for bot messages */}
          {msg.sender === "bot" && (
            <p className="disclaimer-text">
              <strong>Note:</strong> This is an AI-generated response. Always
              consult a healthcare professional for medical advice.
            </p>
          )}
          {msg.sources && (
            <p className="source-text">
              <strong>Source:</strong> {msg.sources.join(", ")}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
