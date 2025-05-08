'use client';

import Image from 'next/image';

export default function Header() {
  return (
    <header className="bg-[#364957] shadow-md fixed w-full top-0 z-10">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Image
          src="/images/kifiya-logo.png"
          alt="Kifiya Logo"
          width={120}
          height={40}
          // Add class if you need to adjust logo color
          className="filter brightness-0 invert-[0.8]" // Optional: Makes logo white/gray
        />
        <h1 className="text-2xl font-bold text-[#FF8A00]">CVForge</h1>
      </div>
    </header>
  );
}