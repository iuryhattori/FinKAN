import {
  ComposedChart, Area, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts';
import { formatTickTime, formatFullTime } from '../../../lib/format';

// Série de preenchimento decorativo: nunca aparece no tooltip.
const AREA_SERIES = 'close-area';

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  const isPrediction = payload[0]?.payload?.isPrediction;
  const rows = payload.filter((p) => p.value != null && p.name !== AREA_SERIES);
  if (!rows.length) return null;

  return (
    <div
      className="rounded p-2.5 text-[11px] shadow-xl border font-data"
      style={{ backgroundColor: 'var(--elevated)', borderColor: 'var(--border-strong)' }}
    >
      <p className="mb-1.5 uppercase tracking-wider text-[9px]" style={{ color: 'var(--muted-foreground)' }}>
        {isPrediction ? `Projeção · ${formatTickTime(label)}` : formatFullTime(label)}
      </p>
      {rows.map((p, i) => (
        <div key={i} className="flex items-center justify-between gap-4">
          <span style={{ color: p.color }}>{p.name}</span>
          <span style={{ color: 'var(--foreground)' }}>R$ {Number(p.value).toFixed(2)}</span>
        </div>
      ))}
    </div>
  );
}

function LegendKey({ color, dashed, children }) {
  return (
    <span className="flex items-center gap-1.5">
      <span
        className={`inline-block w-4 ${dashed ? 'h-0 border-t border-dashed' : 'h-px'}`}
        style={dashed ? { borderColor: color } : { backgroundColor: color }}
      />
      {children}
    </span>
  );
}

export function PredictionChart({ data }) {
  const predIndex = data.findIndex(d => d.isPrediction);

  return (
    <section
      className="panel p-4 h-full"
      aria-label="Gráfico de preço PETR4 — histórico e projeção"
    >
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="section-label mb-0.5">Preço · PETR4</p>
          <p className="text-xs" style={{ color: 'var(--foreground)' }}>
            Evolução da sessão e projeção para a próxima hora
          </p>
        </div>
        <div
          className="flex items-center gap-3 text-[10px]"
          style={{ color: 'var(--muted-foreground)' }}
          aria-hidden="true"
        >
          <LegendKey color="var(--up)">Fechamento</LegendKey>
          <LegendKey color="var(--info)">Abertura</LegendKey>
          <LegendKey color="var(--up)" dashed>Projeção</LegendKey>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <ComposedChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
          <defs>
            <linearGradient id="closeFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="var(--up)" stopOpacity={0.12} />
              <stop offset="100%" stopColor="var(--up)" stopOpacity={0} />
            </linearGradient>
          </defs>
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
            tickFormatter={(v) => v.toFixed(1)}
            width={40}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<ChartTooltip />} />

          {predIndex > 0 && (
            <ReferenceLine
              x={data[predIndex - 1]?.time}
              stroke="rgba(255,255,255,0.12)"
              strokeDasharray="3 3"
              label={{
                value: 'AGORA',
                fill: '#5c6470',
                fontSize: 9,
                fontFamily: 'var(--data-font)',
              }}
            />
          )}

          <Area
            type="monotone"
            dataKey="close"
            name={AREA_SERIES}
            stroke="none"
            fill="url(#closeFill)"
            legendType="none"
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="close"
            stroke="var(--up)"
            strokeWidth={1.5}
            dot={false}
            name="Fechamento"
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="open"
            stroke="var(--info)"
            strokeWidth={1}
            dot={false}
            name="Abertura"
            opacity={0.55}
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="predictedClose"
            stroke="var(--up)"
            strokeWidth={1.5}
            strokeDasharray="4 3"
            dot={{ fill: 'var(--up)', r: 3, strokeWidth: 0 }}
            name="Proj. Fechamento"
          />
          <Line
            type="monotone"
            dataKey="predictedOpen"
            stroke="var(--info)"
            strokeWidth={1}
            strokeDasharray="4 3"
            dot={{ fill: 'var(--info)', r: 3, strokeWidth: 0 }}
            name="Proj. Abertura"
            opacity={0.55}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </section>
  );
}
