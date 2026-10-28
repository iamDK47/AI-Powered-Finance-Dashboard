// Chart libraries (recharts here) render SVG and need literal color
// strings — they can't consume Tailwind utility classes the way JSX
// elements can. These values are kept in sync with the CSS variables in
// app/globals.css by hand; if you change the theme there, update the
// matching values here too. This is the one place in the app where color
// genuinely has to be duplicated for a real technical reason, not an
// oversight.
export const chartColors = {
  background: "#0a0e14",
  surface: "#12171f",
  foreground: "#e6e9ef",
  muted: "#8b95a5",
  line: "#232a36",
  accent: "#22d3a5",
  positive: "#22c55e",
  negative: "#ef4444",
};

// A distinct color per line when plotting multiple assets at once (the
// pct-change comparison chart). Cycles if you plot more assets than
// colors — add more hex values here if you regularly compare more than 6.
export const seriesPalette = [
  "#22d3a5", // accent
  "#60a5fa", // blue
  "#f59e0b", // amber
  "#f472b6", // pink
  "#a78bfa", // violet
  "#facc15", // yellow
];
