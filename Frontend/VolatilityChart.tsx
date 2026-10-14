"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { VolatilityPoint } from "./types";
import { chartColors } from "./chartColors";

interface Props {
  data: VolatilityPoint[];
}

export function VolatilityChart({ data }: Props) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="volatilityFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={chartColors.accent} stopOpacity={0.35} />
              <stop offset="100%" stopColor={chartColors.accent} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke={chartColors.line} />
          <XAxis dataKey="date" stroke={chartColors.muted} tick={{ fontSize: 12 }} />
          <YAxis stroke={chartColors.muted} tick={{ fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              background: chartColors.surface,
              border: `1px solid ${chartColors.line}`,
              borderRadius: 8,
              fontSize: 13,
            }}
          />
          <Area
            type="monotone"
            dataKey="volatility"
            stroke={chartColors.accent}
            strokeWidth={2}
            fill="url(#volatilityFill)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
