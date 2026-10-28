import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "OrderFlow — Crypto Market Dashboard",
  description: "Explore cryptocurrency performance, volatility, and correlation charts.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body className="min-h-screen flex flex-col font-sans"><Header /><main className="flex-1">{children}</main><Footer /></body></html>;
}
