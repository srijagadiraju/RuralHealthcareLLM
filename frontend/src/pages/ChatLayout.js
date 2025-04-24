// src/pages/ChatLayout.js
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import ConfirmModal from "../components/ConfirmModal";
import { Cross } from "lucide-react";

import "../styles/ChatLayout.css";

export default function ChatLayout() {
  const [userId, setUserId] = useState("");
  const [userName, setUserName] = useState("");
  const [chatSessions, setChatSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [showConfirm, setShowConfirm] = useState(false);
  const [chatToDelete, setChatToDelete] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedId = localStorage.getItem("user_id");
    const storedName = localStorage.getItem("name");
    if (storedId) setUserId(storedId);
    if (storedName) setUserName(storedName);
  }, []);

  useEffect(() => {
    if (userId) {
      fetch(`api/chats?user_id=${userId}`)
        .then((res) => res.json())
        .then((data) => setChatSessions(data.sessions || []))
        .catch((err) => {
          console.error("Error loading sessions", err);
          setChatSessions([]);
        });
    }
  }, [userId]);

  useEffect(() => {
    if (selectedSessionId) {
      fetch(`api/chats/${selectedSessionId}/messages`)
        .then((res) => res.json())
        .then((data) => setMessages(data.messages || []))
        .catch((err) => {
          console.error("Error loading messages", err);
          setMessages([]);
        });
    }
  }, [selectedSessionId]);

  const handleSelectSession = (sessionId) => {
    setSelectedSessionId(sessionId);
  };

  const handleSend = async (userInput) => {
    const userMsg = { sender: "user", text: userInput };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);

    try {
      const res = await fetch(
        `api/generate-answer?query=${encodeURIComponent(userInput)}`
      );
      const data = await res.json();
      const botMsg = { sender: "bot", text: data.generated_answer };
      const updatedMessages = [...newMessages, botMsg];
      setMessages(updatedMessages);

      await fetch(`api/chats/${selectedSessionId}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userMsg),
      });

      await fetch(`api/chats/${selectedSessionId}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(botMsg),
      });
      // Fetches updated chat list and move the current chat to the top
      const updatedSessions = await fetch(`api/chats?user_id=${userId}`);
      const updatedData = await updatedSessions.json();
      const reordered = updatedData.sessions?.filter(
        (s) => s._id !== selectedSessionId
      );
      const current = updatedData.sessions?.find(
        (s) => s._id === selectedSessionId
      );
      setChatSessions(
        current ? [current, ...(reordered || [])] : updatedData.sessions || []
      );
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, something went wrong." },
      ]);
    }
  };

  const handleNewChat = async () => {
    const title = `Chat ${(chatSessions || []).length + 1}`;
    const res = await fetch("api/chats/new", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, title }),
    });

    const data = await res.json();
    const newSession = {
      _id: data.chat_id,
      title,
      user_id: userId,
      created_at: new Date().toISOString(),
    };

    setChatSessions((prev) => [newSession, ...prev]);
    setSelectedSessionId(data.chat_id);
    setMessages([]);
  };

  const confirmDeleteChat = (chatId) => {
    setChatToDelete(chatId);
    setShowConfirm(true);
  };

  const handleDeleteConfirmed = async () => {
    try {
      const res = await fetch(`api/chats/${chatToDelete}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete chat");

      setChatSessions((prev) => prev.filter((s) => s._id !== chatToDelete));

      if (chatToDelete === selectedSessionId) {
        setSelectedSessionId(null);
        setMessages([]);
      }
    } catch (err) {
      console.error("Error deleting chat:", err);
    } finally {
      setShowConfirm(false);
      setChatToDelete(null);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <div className="chat-layout">
      <header className="chat-header">
        <div className="welcome-text">Welcome, {userName}!</div>
        <div className="chat-title">
          <Cross size={40} style={{ marginRight: "8px" }} color="#005fb8" />
          CareGPT
        </div>
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <div className="chat-body">
        <Sidebar
          chatSessions={chatSessions || []}
          onSelectSession={handleSelectSession}
          onNewChat={handleNewChat}
          selectedSessionId={selectedSessionId}
          onDeleteSession={confirmDeleteChat}
        />
        <div className="chat-area">
          {selectedSessionId ? (
            <>
              <ChatWindow messages={messages || []} />
              <ChatInput onSend={handleSend} />
            </>
          ) : (
            <div className="empty-chat-container">
              <img
                src="/assets/friendly-bot.png"
                alt="Friendly Chatbot"
                className="friendly-bot-img"
              />
              <p className="empty-chat-text">
                Click <strong>+ New Chat</strong> to start your medical
                conversation!
              </p>
            </div>
          )}
        </div>
      </div>

      {showConfirm && (
        <ConfirmModal
          message="Are you sure you want to delete this chat?"
          onConfirm={handleDeleteConfirmed}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </div>
  );
}
