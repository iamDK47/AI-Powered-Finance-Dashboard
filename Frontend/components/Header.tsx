"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/charts", label: "Charts" },
];

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="border-b border-line bg-surface/80 backdrop-blur sticky top-0 z-50">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 flex items-center justify-between h-16">
        <Link href="/" className="font-semibold text-lg tracking-tight text-foreground">
          Order<span className="text-accent">Flow</span>
        </Link>
        <nav className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map(link => (
            <Link key={link.href} href={link.href} className={`px-3 py-2 rounded-md text-sm transition-colors ${pathname === link.href ? "text-accent bg-accent/10" : "text-muted hover:text-foreground hover:bg-surface-hover"}`}>
              {link.label}
            </Link>
          ))}
        </nav>
        <button className="md:hidden text-foreground" onClick={() => setMobileOpen(value => !value)} aria-label="Toggle menu" aria-expanded={mobileOpen}>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {mobileOpen ? <path d="M18 6L6 18M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" /> : <path d="M3 6h18M3 12h18M3 18h18" strokeLinecap="round" strokeLinejoin="round" />}
          </svg>
        </button>
      </div>
      {mobileOpen && (
        <nav className="md:hidden border-t border-line px-4 py-3 flex flex-col gap-1">
          {NAV_LINKS.map(link => (
            <Link key={link.href} href={link.href} onClick={() => setMobileOpen(false)} className={`px-3 py-2 rounded-md text-sm ${pathname === link.href ? "text-accent bg-accent/10" : "text-muted"}`}>
              {link.label}
            </Link>
          ))}
        </nav>
      )}
    </header>
  );
}
