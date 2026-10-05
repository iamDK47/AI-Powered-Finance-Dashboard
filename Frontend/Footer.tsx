// Edit the details in this object — nothing else in this file needs to
// change to update the footer's content.
const FOOTER_DETAILS = {
  name: "Daniyal", // your name
  role: "Building fintech & trading-systems software",
  github: "https://github.com/your-username",
  linkedin: "https://linkedin.com/in/your-username",
  email: "you@example.com",
};

export function Footer() {
  return (
    <footer className="border-t border-line mt-16">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 py-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted">
        <div>
          <p className="text-foreground font-medium">{FOOTER_DETAILS.name}</p>
          <p>{FOOTER_DETAILS.role}</p>
        </div>
        <div className="flex gap-4">
          <a href={FOOTER_DETAILS.github} className="hover:text-foreground transition-colors">
            GitHub
          </a>
          <a href={FOOTER_DETAILS.linkedin} className="hover:text-foreground transition-colors">
            LinkedIn
          </a>
          <a href={`mailto:${FOOTER_DETAILS.email}`} className="hover:text-foreground transition-colors">
            Email
          </a>
        </div>
        <p>&copy; {new Date().getFullYear()} {FOOTER_DETAILS.name}</p>
      </div>
    </footer>
  );
}
