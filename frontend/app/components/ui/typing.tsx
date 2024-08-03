import React from 'react';

interface TypingTextProps {
  text: string;
  speed?: number;
}

export function TypingText({ text }: TypingTextProps) {
  return (
    <span className="inline-block overflow-hidden whitespace-nowrap border-r-2 border-r-white animate-typing">
      {text}
      <span className="animate-blink">|</span>
    </span>
  );
}
