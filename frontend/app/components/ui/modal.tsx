import * as React from "react";
import { useEffect } from "react";

interface ModalProps {
  isVisible: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

const Modal = ({ isVisible, onClose, children }: ModalProps) => {
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };
    if (isVisible) {
      document.addEventListener("keydown", handleEscape);
    } else {
      document.removeEventListener("keydown", handleEscape);
    }
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isVisible, onClose]);

  if (!isVisible) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      onClick={onClose}
    >
      <div
        className="p-6 rounded-lg shadow-lg w-full max-w-3xl bg-primary-foreground overflow-y-auto max-h-full"
        onClick={(e) => e.stopPropagation()}
      >
        <button onClick={onClose} className="float-right text-gray-700">
          &times;
        </button>
        {children}
      </div>
    </div>
  );
};

export { Modal };
