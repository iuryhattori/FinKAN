import { ArrowRight, TrendingUp, TrendingDown, Minus } from 'lucide-react';

export function PredictionCard({ label, current, predicted }) {
  const change = predicted - current;
  const changePercent = (change / current) * 100;
  const isFlat = Math.abs(changePercent) < 0.05;
  const isPositive = change >= 0;
  const tone = isFlat ? 'var(--muted-foreground)' : isPositive ? 'var(--up)' : 'var(--down)';
  const toneBg = isFlat ? 'var(--secondary)' : isPositive ? 'var(--up-bg)' : 'var(--down-bg)';
  const TrendIcon = isFlat ? Minus : isPositive ? TrendingUp : TrendingDown;

  const fmt = (v) => `R$ ${v.toFixed(2)}`;

  return (
    <article
      className="panel p-3.5 flex flex-col gap-3"
      aria-label={`${label} forecast for the next hour`}
    >
      <div className="flex items-center justify-between">
        <span className="section-label">{label}</span>
        <span
          className="flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded-sm font-data"
          style={{ color: tone, backgroundColor: toneBg }}
          aria-label={`Forecast change: ${isPositive ? '+' : ''}${changePercent.toFixed(2)}%`}
        >
          <TrendIcon className="w-2.5 h-2.5" aria-hidden="true" />
          {isPositive ? '+' : ''}{changePercent.toFixed(2)}%
        </span>
      </div>

      <div className="flex items-center justify-between gap-2">
        <div className="leading-tight">
          <p className="text-[10px] mb-0.5" style={{ color: 'var(--muted-foreground)' }}>
            Now
          </p>
          <p className="text-xs font-data" style={{ color: 'var(--secondary-foreground)' }}>
            {fmt(current)}
          </p>
        </div>
        <ArrowRight className="w-3 h-3 flex-none" style={{ color: 'var(--faint)' }} aria-hidden="true" />
        <div className="leading-tight text-right">
          <p className="text-[10px] mb-0.5" style={{ color: 'var(--muted-foreground)' }}>
            In 1 hour
          </p>
          <p className="text-sm font-semibold font-data" style={{ color: tone }}>
            {fmt(predicted)}
          </p>
        </div>
      </div>

      <div
        className="h-0.5 rounded-full overflow-hidden"
        style={{ backgroundColor: 'var(--secondary)' }}
        role="progressbar"
        aria-valuenow={Math.min(Math.abs(changePercent) * 20, 100)}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{
            width: `${Math.min(Math.abs(changePercent) * 20, 100)}%`,
            backgroundColor: tone,
          }}
        />
      </div>
    </article>
  );
}
