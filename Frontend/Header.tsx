"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useAuth } from "./AuthProvider";

// Edit this array to add, remove, or reorder header routes — the nav bar
// (desktop and mobile both) renders directly from this list, so you never
// need to touch the JSX below to change what pages appear in the header.
const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/charts", label: "Charts" },
];

export function Header() {
  const pathname = usePathname();
  const { user, isGuest, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="border-b border-line bg-surface/80 backdrop-blur sticky top-0 z-50">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 flex items-center justify-between h-16">
        <Link href="/" className="font-semibold text-lg tracking-tight text-foreground">
          {/* Edit this product name in one place */}
          Order<span className="text-accent">Flow</span>
        </Link>

        <nav className="hidden md:flex items-center gap-1">
          {NAV_LINKS.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-2 rounded-md text-sm transition-colors ${
                  active
                    ? "text-accent bg-accent/10"
                    : "text-muted hover:text-foreground hover:bg-surface-hover"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <>
              <span className="text-sm text-muted">{user.username}</span>
              <button
                onClick={logout}
                className="text-sm px-3 py-1.5 rounded-md border border-line text-muted hover:text-foreground hover:border-foreground/30 transition-colors"
              >
                Log out
              </button>
            </>
          ) : isGuest ? (
            <>
              <span className="text-sm text-muted">Guest mode</span>
              <Link
                href="/login"
                className="text-sm px-3 py-1.5 rounded-md bg-accent text-background font-medium hover:bg-accent-hover transition-colors"
              >
                Sign in
              </Link>
            </>
          ) : (
            <Link
              href="/login"
              className="text-sm px-3 py-1.5 rounded-md bg-accent text-background font-medium hover:bg-accent-hover transition-colors"
            >
              Sign in
            </Link>
          )}
        </div>

        <button
          className="md:hidden text-foreground"
          onClick={() => setMobileOpen((v) => !v)}
          aria-label="Toggle menu"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {mobileOpen ? (
              <path d="M18 6L6 18M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" />
            ) : (
              <path d="M3 6h18M3 12h18M3 18h18" strokeLinecap="round" strokeLinejoin="round" />
            )}
          </svg>
        </button>
      </div>

      {mobileOpen && (
        <div className="md:hidden border-t border-line px-4 py-3 flex flex-col gap-1">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className={`px-3 py-2 rounded-md text-sm ${
                pathname === link.href ? "text-accent bg-accent/10" : "text-muted"
              }`}
            >
              {link.label}
            </Link>
          ))}
          <div className="pt-2 mt-2 border-t border-line">
            {user ? (
              <button onClick={logout} className="text-sm text-muted px-3 py-2">
                Log out ({user.username})
              </button>
            ) : (
              <Link href="/login" className="text-sm text-accent px-3 py-2 block">
                Sign in
              </Link>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
