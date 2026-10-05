import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/components/AuthProvider";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

// Deliberately NOT using next/font/google here. next/font/google fetches
// the font file at BUILD time from Google's servers — fine on a normal
// connection, but it means your build can fail behind a restrictive
// firewall, in some CI environments, or if Google's fonts CDN has a bad
// moment. A system font stack has zero external dependency and zero
// build-time network risk, at the cost of the page looking very slightly
// different across operating systems. If you want a specific custom font
// later, next/font/local (self-hosting the font file in this repo) gets
// you the same optimization without the build-time fetch.

// Edit title/description here — this is what shows in browser tabs and
// search/social previews.
export const metadata: Metadata = {
  title: "OrderFlow — Crypto Market Analytics",
  description: "Volatility, correlation, and order-flow analytics across crypto assets.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      {/* AuthProvider wraps EVERYTHING so any page or component can call
          useAuth() — this is what makes login state available across
          Header, every page, and any component you add later, without
          passing it down manually through props. */}
      <body className="min-h-full flex flex-col font-sans">
        <AuthProvider>
          <Header />
          <main className="flex-1 w-full">{children}</main>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
