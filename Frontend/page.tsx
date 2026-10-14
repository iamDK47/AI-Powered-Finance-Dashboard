import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 lg:py-24">
      <section className="max-w-3xl">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-accent">OrderFlow · Crypto market dashboard</p>
        <h1 className="mt-5 text-5xl font-semibold tracking-tight text-foreground sm:text-7xl">See the market <span className="text-accent">in motion.</span></h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-muted">Compare price performance, explore rolling volatility, and see how crypto assets move together. Sign in to connect your market database, or use guest mode to explore with sample data.</p>
        <div className="mt-9 flex flex-wrap gap-3">
          <Link href="/login" className="rounded-md bg-accent px-5 py-3 font-semibold text-background hover:bg-accent-hover">Get started</Link>
          <Link href="/charts" className="rounded-md border border-line px-5 py-3 font-semibold text-foreground hover:bg-surface">Open charts</Link>
        </div>
      </section>
      <section className="mt-20 grid gap-4 sm:grid-cols-3">
        {[
          ["Performance", "Compare normalized percentage moves across available assets."],
          ["Volatility", "Follow rolling daily return volatility for a selected ticker."],
          ["Correlation", "Explore the relationship between daily asset returns."],
        ].map(([title, text]) => <article key={title} className="rounded-xl border border-line bg-surface p-6"><h2 className="font-semibold">{title}</h2><p className="mt-2 text-sm leading-6 text-muted">{text}</p></article>)}
      </section>
    </div>
  );
}
