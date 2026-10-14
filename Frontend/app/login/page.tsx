"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { useAuth } from "../../AuthProvider";

export default function LoginPage() {
  const { login, continueAsGuest } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError("");
    try { await login(username, password); router.push("/charts"); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not sign in. Check the API is running."); }
    finally { setBusy(false); }
  }

  function guest() { continueAsGuest(); router.push("/charts"); }

  return <div className="mx-auto max-w-md px-4 py-16 sm:py-24">
    <Link href="/" className="text-sm text-muted hover:text-foreground">← Back to home</Link>
    <div className="mt-6 rounded-xl border border-line bg-surface p-7">
      <p className="text-sm font-semibold uppercase tracking-widest text-accent">Welcome</p>
      <h1 className="mt-2 text-3xl font-semibold">Sign in to OrderFlow</h1>
      <p className="mt-2 text-sm leading-6 text-muted">Use the admin username and password configured for your FastAPI backend.</p>
      <form onSubmit={submit} className="mt-7 space-y-4">
        <label className="block text-sm">Username<input autoComplete="username" required value={username} onChange={e => setUsername(e.target.value)} className="mt-1.5 w-full rounded-md border border-line bg-background px-3 py-2.5 outline-none focus:border-accent" /></label>
        <label className="block text-sm">Password<input type="password" autoComplete="current-password" required value={password} onChange={e => setPassword(e.target.value)} className="mt-1.5 w-full rounded-md border border-line bg-background px-3 py-2.5 outline-none focus:border-accent" /></label>
        {error && <p role="alert" className="rounded-md border border-negative/40 bg-negative/10 p-3 text-sm text-negative">{error}</p>}
        <button disabled={busy} className="w-full rounded-md bg-accent px-4 py-3 font-semibold text-background disabled:opacity-60">{busy ? "Signing in…" : "Sign in"}</button>
      </form>
      <div className="my-5 flex items-center gap-3 text-xs text-muted"><span className="h-px flex-1 bg-line" />OR<span className="h-px flex-1 bg-line" /></div>
      <button onClick={guest} className="w-full rounded-md border border-line px-4 py-3 font-medium hover:bg-surface-hover">Continue as guest</button>
      <p className="mt-4 text-xs leading-5 text-muted">Guest mode uses generated sample figures. It does not create an account or call your backend.</p>
    </div>
  </div>;
}
