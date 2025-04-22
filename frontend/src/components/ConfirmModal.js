// src/components/ConfirmModal.js
import React from "react";
import "../styles/ConfirmModal.css";

export default function ConfirmModal({ onConfirm, onCancel, message }) {
  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <p className="modal-message">{message}</p>

        <div className="modal-buttons">
          <button className="cancel-btn" onClick={onCancel}>
            Cancel
          </button>
          <button className="delete-btn" onClick={onConfirm}>
            Yes, Delete
          </button>
        </div>
      </div>
    </div>
  );
}
