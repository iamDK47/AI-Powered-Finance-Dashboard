"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { PctChangePoint } from "@/lib/types";
import { chartColors, seriesPalette } from "@/lib/chartColors";

interface Props {
  data: PctChangePoint[];
  tickers: string[];
}

export function PctChangeLines({ data, tickers }: Props) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={chartColors.line} />
          <XAxis dataKey="date" stroke={chartColors.muted} tick={{ fontSize: 12 }} />
          <YAxis
            stroke={chartColors.muted}
            tick={{ fontSize: 12 }}
            tickFormatter={(v) => `${v}%`}
          />
          <Tooltip
            contentStyle={{
              background: chartColors.surface,
              border: `1px solid ${chartColors.line}`,
              borderRadius: 8,
              fontSize: 13,
            }}
            formatter={(value) => `${Number(value).toFixed(2)}%`}
          />
          <Legend wrapperStyle={{ fontSize: 12, color: chartColors.muted }} />
          {tickers.map((ticker, i) => (
            <Line
              key={ticker}
              type="monotone"
              dataKey={ticker}
              stroke={seriesPalette[i % seriesPalette.length]}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
