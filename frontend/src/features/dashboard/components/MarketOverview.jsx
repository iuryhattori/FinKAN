import { TrendingUp, TrendingDown } from 'lucide-react';
import { formatVolume } from '../../../lib/format';

function StatCell({ label, value, color, isLast }) {
  return (
    <div
      className={`px-4 py-3 ${!isLast ? 'border-r' : ''}`}
      style={{ borderColor: 'var(--panel-border)' }}
    >
      <p className="section-label mb-1">{label}</p>
      <p className="text-sm font-data" style={{ color: color || 'var(--foreground)' }}>
        {value}
      </p>
    </div>
  );
}

/** Posição do preço atual dentro da faixa do período (mínima → máxima). */
function DayRangeBar({ low, high, close }) {
  const span = high - low;
  const position = span > 0 ? Math.min(Math.max((close - low) / span, 0), 1) : 0.5;

  return (
    <div className="flex items-center gap-3 min-w-[220px]" aria-label="Position within session range">
      <span className="text-[10px] font-data" style={{ color: 'var(--down)' }}>
        {low.toFixed(2)}
      </span>
      <div className="relative flex-1 h-1 rounded-full" style={{ backgroundColor: 'var(--secondary)' }}>
        <div
          className="absolute top-1/2 -translate-y-1/2 w-2 h-2 rounded-full border-2"
          style={{
            left: `calc(${(position * 100).toFixed(1)}% - 4px)`,
            backgroundColor: 'var(--foreground)',
            borderColor: 'var(--background)',
          }}
        />
      </div>
      <span className="text-[10px] font-data" style={{ color: 'var(--up)' }}>
        {high.toFixed(2)}
      </span>
    </div>
  );
}

export function MarketOverview({ currentData }) {
  const dayChange = currentData.close - currentData.open;
  const dayChangePct = (dayChange / currentData.open) * 100;
  const isUp = dayChange >= 0;
  const TrendIcon = isUp ? TrendingUp : TrendingDown;

  const stats = [
    { label: 'Open', value: `R$ ${currentData.open.toFixed(2)}` },
    { label: 'Close', value: `R$ ${currentData.close.toFixed(2)}` },
    { label: 'High', value: `R$ ${currentData.high.toFixed(2)}`, color: 'var(--up)' },
    { label: 'Low', value: `R$ ${currentData.low.toFixed(2)}`, color: 'var(--down)' },
    { label: 'Volume (ticks)', value: formatVolume(currentData.volume) },
  ];

  // timeZone UTC: o timestamp do MT5 já é o relógio do pregão (ver lib/format.js)
  const updatedAt = currentData.date
    ? currentData.date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'UTC' })
    : null;

  return (
    <section className="panel overflow-hidden" aria-label="PETR4 market overview">
      <div className="flex items-start justify-between p-5 pb-4">
        <div>
          <div className="flex items-center gap-2.5 mb-1">
            <h1 className="text-sm font-semibold tracking-wide" style={{ color: 'var(--foreground)' }}>
              Petrobras PN
            </h1>
            <span
              className="text-[10px] px-1.5 py-0.5 rounded-sm font-data"
              style={{ backgroundColor: 'var(--secondary)', color: 'var(--secondary-foreground)' }}
            >
              PETR4
            </span>
            <span
              className="text-[10px] px-1.5 py-0.5 rounded-sm"
              style={{ backgroundColor: 'var(--secondary)', color: 'var(--secondary-foreground)' }}
            >
              B3
            </span>
          </div>

          <div className="flex items-baseline gap-3">
            <span className="text-[32px] font-semibold font-data" style={{ color: 'var(--foreground)' }}>
              R$ {currentData.close.toFixed(2)}
            </span>
            <span
              className="flex items-center gap-1.5 text-sm font-data px-2 py-0.5 rounded"
              style={{
                color: isUp ? 'var(--up)' : 'var(--down)',
                backgroundColor: isUp ? 'var(--up-bg)' : 'var(--down-bg)',
              }}
            >
              <TrendIcon className="w-3.5 h-3.5" aria-hidden="true" />
              {isUp ? '+' : ''}{dayChange.toFixed(2)} ({isUp ? '+' : ''}{dayChangePct.toFixed(2)}%)
            </span>
          </div>

          <p className="text-[10px] mt-1.5" style={{ color: 'var(--muted-foreground)' }}>
            {updatedAt
              ? `Last candle at ${updatedAt} · change vs. period open`
              : 'Change vs. period open'}
          </p>
        </div>

        <div className="flex flex-col items-end gap-3 pt-1">
          <span className="section-label">Session range</span>
          <DayRangeBar low={currentData.low} high={currentData.high} close={currentData.close} />
        </div>
      </div>

      <div
        className="grid grid-cols-5 border-t"
        style={{ borderColor: 'var(--panel-border)', backgroundColor: 'var(--muted)' }}
      >
        {stats.map((stat, i) => (
          <StatCell
            key={stat.label}
            label={stat.label}
            value={stat.value}
            color={stat.color}
            isLast={i === stats.length - 1}
          />
        ))}
      </div>
    </section>
  );
}
