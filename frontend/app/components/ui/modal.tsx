import * as React from "react"
import { Button } from "@/app/components/ui/button";

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
      <div className="p-6 rounded-lg shadow-lg w-2/5 max-w-3xl bg-primary-foreground">
        <Button onClick={onClose} className="float-right text-gray-700">
          &times;
        </Button>
        {children}
      </div>
    </div>
  );
};

export {Modal};
