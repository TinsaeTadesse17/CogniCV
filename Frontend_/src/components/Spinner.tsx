import React from 'react';

interface SpinnerProps {
  className?: string;
}

export default function Spinner({ className = '' }: SpinnerProps) {
  return (
    <div className={`border-4 border-[#FF8A00] border-t-transparent rounded-full animate-spin animate-fadeIn ${className}`} />
  );
}