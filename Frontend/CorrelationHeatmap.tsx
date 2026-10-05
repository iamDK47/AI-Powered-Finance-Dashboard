"use client";

import { CorrelationMatrix } from "@/lib/types";
import { chartColors } from "@/lib/chartColors";

interface Props {
  matrix: CorrelationMatrix;
}

// Correlation heatmaps aren't a built-in recharts chart type, so this is a
// plain CSS grid instead — colors interpolated by hand rather than pulled
// from a charting library. Diverging scale: negative correlation shades
// toward red, positive shades toward green, and near-zero stays close to
// the neutral surface color.
function cellColor(value: number): string {
  const alpha = Math.round(Math.abs(value) * 200)
    .toString(16)
    .padStart(2, "0");
  const base = value >= 0 ? chartColors.positive : chartColors.negative;
  return `${base}${alpha}`;
}

export function CorrelationHeatmap({ matrix }: Props) {
  const { tickers, values } = matrix;

  return (
    <div className="overflow-x-auto">
      <div
        className="grid gap-px bg-line min-w-max"
        style={{ gridTemplateColumns: `120px repeat(${tickers.length}, 64px)` }}
      >
        <div className="bg-surface" />
        {tickers.map((t) => (
          <div
            key={`col-${t}`}
            className="bg-surface text-[11px] text-muted flex items-end justify-center pb-1 px-1 text-center"
          >
            {t.replace("USDT", "")}
          </div>
        ))}

        {tickers.map((rowTicker, i) => (
          <div key={`row-${rowTicker}`} className="contents">
            <div className="bg-surface text-[11px] text-muted flex items-center px-2">
              {rowTicker.replace("USDT", "")}
            </div>
            {values[i].map((value, j) => (
              <div
                key={`${i}-${j}`}
                title={`${rowTicker} vs ${tickers[j]}: ${value.toFixed(2)}`}
                className="aspect-square flex items-center justify-center text-[11px] text-foreground cursor-default"
                style={{ backgroundColor: cellColor(value) }}
              >
                {value.toFixed(2)}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
