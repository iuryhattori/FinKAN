import { BarChart3 } from 'lucide-react';

function isMarketOpen(time) {
  const h = time.getHours();
  const m = time.getMinutes();
  const total = h * 60 + m;
  return total >= 10 * 60 && total < 17 * 60 + 30;
}

const connectionConfig = {
  live: { label: 'Live', color: 'var(--up)', pulse: true },
  loading: { label: 'Connecting…', color: 'var(--warn)', pulse: true },
  reconnecting: { label: 'Reconnecting…', color: 'var(--warn)', pulse: true },
  error: { label: 'Offline', color: 'var(--down)', pulse: false },
};

function StatusDot({ color, pulse }) {
  return (
    <span className="relative inline-flex w-2 h-2" aria-hidden="true">
      {pulse && (
        <span
          className="absolute inline-flex w-full h-full rounded-full animate-ping opacity-40"
          style={{ backgroundColor: color }}
        />
      )}
      <span
        className="relative inline-flex w-2 h-2 rounded-full"
        style={{ backgroundColor: color }}
      />
    </span>
  );
}

export function Header({ currentTime, connectionStatus = 'loading' }) {
  const open = isMarketOpen(currentTime);
  const connection = connectionConfig[connectionStatus] ?? connectionConfig.loading;

  return (
    <header
      className="border-b px-6"
      style={{ backgroundColor: '#0d0f15', borderColor: 'var(--panel-border)' }}
    >
      <div className="max-w-[1600px] mx-auto flex items-center justify-between h-14">
        {/* Marca */}
        <div className="flex items-center gap-3">
          <div
            className="flex items-center justify-center w-8 h-8 rounded"
            style={{ backgroundColor: 'var(--brand-muted)' }}
          >
            <BarChart3 className="w-4 h-4" style={{ color: 'var(--brand)' }} aria-hidden="true" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-semibold tracking-wide" style={{ color: 'var(--foreground)' }}>
              FinKAN
            </p>
            <p className="text-[10px] tracking-wider" style={{ color: 'var(--muted-foreground)' }}>
              Predictive market analytics
            </p>
          </div>
        </div>

        {/* Contexto da sessão */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <StatusDot color={open ? 'var(--up)' : 'var(--faint)'} pulse={open} />
            <div className="leading-tight">
              <p className="text-xs" style={{ color: 'var(--foreground)' }}>
                {open ? 'Market open' : 'Market closed'}
              </p>
              <p className="text-[10px]" style={{ color: 'var(--muted-foreground)' }}>
                {open ? 'B3 · closes at 17:30' : 'B3 · opens at 10:00'}
              </p>
            </div>
          </div>

          <div className="h-6 w-px" style={{ backgroundColor: 'var(--border)' }} />

          <div className="flex items-center gap-2">
            <StatusDot color={connection.color} pulse={connection.pulse} />
            <div className="leading-tight">
              <p className="text-xs" style={{ color: 'var(--foreground)' }}>
                {connection.label}
              </p>
              <p className="text-[10px]" style={{ color: 'var(--muted-foreground)' }}>
                Data via MetaTrader 5
              </p>
            </div>
          </div>

          <div className="h-6 w-px" style={{ backgroundColor: 'var(--border)' }} />

          <div className="leading-tight text-right">
            <p className="text-xs font-data" style={{ color: 'var(--foreground)' }}>
              {currentTime.toLocaleTimeString('en-GB')}
            </p>
            <p className="text-[10px]" style={{ color: 'var(--muted-foreground)' }}>
              Forecast horizon · 1h
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}
