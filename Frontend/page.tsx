import Link from "next/link";

// This entire page is placeholder copy — rewrite the text below to
// describe your actual product. The structure (hero, feature cards)
// is reusable; only the words need to change.
export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6 py-16">
      <section className="max-w-2xl">
        <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight text-foreground">
          Read the market&apos;s{" "}
          <span className="text-accent">order flow</span>, not just its price.
        </h1>
        <p className="mt-5 text-lg text-muted leading-relaxed">
          OrderFlow pulls 1-minute granular data across major crypto assets and
          turns it into volatility, correlation, and momentum views built on
          real market-microstructure methodology — not just a candlestick
          chart with extra steps.
        </p>
        <div className="mt-8 flex gap-3">
          <Link
            href="/charts"
            className="px-5 py-2.5 rounded-md bg-accent text-background font-medium hover:bg-accent-hover transition-colors"
          >
            View live charts
          </Link>
          <Link
            href="/docs"
            className="px-5 py-2.5 rounded-md border border-line text-foreground hover:border-foreground/30 transition-colors"
          >
            Read the methodology
          </Link>
        </div>
      </section>

      <section className="mt-20 grid sm:grid-cols-3 gap-4">
        {[
          {
            title: "Volatility tracking",
            body: "Rolling volatility across assets, so you can see when the market is genuinely calm versus quietly coiling.",
          },
          {
            title: "Cross-asset correlation",
            body: "A live correlation matrix — know when your 'diversified' basket is actually just one trade in disguise.",
          },
          {
            title: "Normalized performance",
            body: "Percent-change-from-start overlays across multiple assets, so relative strength is visible at a glance.",
          },
        ].map((card) => (
          <div key={card.title} className="rounded-lg border border-line bg-surface p-5">
            <h3 className="font-medium text-foreground">{card.title}</h3>
            <p className="mt-2 text-sm text-muted leading-relaxed">{card.body}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
