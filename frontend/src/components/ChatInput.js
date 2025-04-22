import React, { useState } from "react";
import "../styles/ChatInput.css";

export default function ChatInput({ onSend }) {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    if (input.trim() !== "") {
      onSend(input);
      setInput("");
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        placeholder="Ask a medical question..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
      />
      <button onClick={handleSubmit}>Ask</button>
    </div>
  );
}
