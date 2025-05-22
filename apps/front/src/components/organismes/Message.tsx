import React, { useEffect, useState } from "react"

type BlocMessageProps = {
  message: string;
  durationMs?: number; // durée avant disparition en ms (défaut 3000)
  onClose?: () => void; // callback optionnel à la fermeture
};

export function Message({ message, durationMs = 3000, onClose }: BlocMessageProps) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setVisible(false);
      if (onClose) onClose();
    }, durationMs);

    return () => clearTimeout(timeout);
  }, [durationMs, onClose]);

  if (!visible) return null;

  return (
    <div
      role="alert"
      className="fixed top-10 left-1/2 transform -translate-x-1/2 bg-green-600 text-white px-4 py-2 rounded shadow-md"
    >
      {message}
    </div>
  );
}
