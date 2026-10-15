"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState, ReactNode } from "react";
import { login as apiLogin } from "./api";
import { AuthUser } from "./types";

interface AuthContextValue {
  user: AuthUser | null;
  isGuest: boolean;
  isLoading: boolean; // true only during the initial localStorage check on first load
  login: (username: string, password: string) => Promise<void>;
  continueAsGuest: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const STORAGE_KEY = "crypto-dashboard-auth";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isGuest, setIsGuest] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Runs once, client-side only, after the initial render. Next.js
  // server-renders this component first (where `window`/`localStorage`
  // don't exist), so reading localStorage has to happen in an effect,
  // never during render — doing it during render is what causes
  // "hydration mismatch" errors, where the server HTML and the first
  // client render disagree.
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      }
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const { access_token } = await apiLogin(username, password);
    const authUser: AuthUser = { username, token: access_token };
    setUser(authUser);
    setIsGuest(false);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(authUser));
  }, []);

  const continueAsGuest = useCallback(() => {
    setIsGuest(true);
    setUser(null);
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    setIsGuest(false);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const value = useMemo(() => ({ user, isGuest, isLoading, login, continueAsGuest, logout }), [user, isGuest, isLoading, login, continueAsGuest, logout]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside <AuthProvider>");
  }
  return ctx;
}
