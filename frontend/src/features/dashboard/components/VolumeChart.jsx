import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from 'recharts';
import { formatVolume, formatTickTime, formatFullTime } from '../../../lib/format';

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div
      className="rounded p-2.5 text-[11px] shadow-xl border font-data"
      style={{ backgroundColor: 'var(--elevated)', borderColor: 'var(--border-strong)' }}
    >
      <p className="mb-1.5 uppercase tracking-wider text-[9px]" style={{ color: 'var(--muted-foreground)' }}>
        {formatFullTime(label)}
      </p>
      {payload.map((p, i) => (
        <div key={i} className="flex items-center justify-between gap-4">
          <span style={{ color: 'var(--info)' }}>{p.name}</span>
          <span style={{ color: 'var(--foreground)' }}>{formatVolume(p.value)}</span>
        </div>
      ))}
    </div>
  );
}

export function VolumeChart({ data }) {
  return (
    <section
      className="panel p-4 h-full"
      aria-label="Gráfico de volume de negociação PETR4"
    >
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="section-label mb-0.5">Volume · PETR4</p>
          <p className="text-xs" style={{ color: 'var(--foreground)' }}>
            Intensidade de negociação por candle
          </p>
        </div>
        <div
          className="flex items-center gap-1.5 text-[10px]"
          style={{ color: 'var(--muted-foreground)' }}
          aria-hidden="true"
        >
          <span className="inline-block w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: 'var(--info)', opacity: 0.7 }} />
          Ticks negociados
        </div>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }} barCategoryGap="30%">
          <CartesianGrid
            strokeDasharray="2 4"
            stroke="rgba(255,255,255,0.04)"
            vertical={false}
          />
          <XAxis
            dataKey="time"
            tick={{ fill: '#5c6470', fontSize: 10, fontFamily: 'var(--data-font)' }}
            axisLine={{ stroke: 'rgba(255,255,255,0.06)' }}
            tickLine={false}
            tickFormatter={formatTickTime}
            minTickGap={48}
            interval="preserveStartEnd"
          />
          <YAxis
            tick={{ fill: '#5c6470', fontSize: 10, fontFamily: 'var(--data-font)' }}
            axisLine={false}
            tickLine={false}
            tickFormatter={formatVolume}
            width={42}
          />
          <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
          <Bar
            dataKey="volume"
            name="Volume"
            fill="var(--info)"
            opacity={0.55}
            radius={[2, 2, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </section>
  );
}
