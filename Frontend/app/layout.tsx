import type { Metadata } from "next";
import "../globals.css";
import { AuthProvider } from "../AuthProvider";
import { Header } from "../Header";
import { Footer } from "../Footer";

export const metadata: Metadata = {
  title: "OrderFlow — Crypto Market Dashboard",
  description: "Explore cryptocurrency performance, volatility, and correlation charts.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body className="min-h-screen flex flex-col font-sans"><AuthProvider><Header /><main className="flex-1">{children}</main><Footer /></AuthProvider></body></html>;
}
