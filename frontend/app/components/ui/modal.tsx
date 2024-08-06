import * as React from "react"

interface ModalProps {
  isVisible: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

const Modal = ({ isVisible, onClose, children }: ModalProps) => {
  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center">
      <div className="p-6 rounded-lg shadow-lg w-full max-w-3xl bg-primary-foreground">
        <button onClick={onClose} className="float-right text-gray-700">
          &times;
        </button>
        {children}
      </div>
    </div>
  );
};

export {Modal};
