import { useState, useEffect } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';
import { tickerItems } from '../data/mock';

export function TickerStrip({ currentTime }) {
  const [tickerOffset, setTickerOffset] = useState(0);

  useEffect(() => {
    const ticker = setInterval(() => {
      setTickerOffset(prev => (prev + 1) % (tickerItems.length * 160));
    }, 40);
    return () => clearInterval(ticker);
  }, []);

  return (
    <div
      className="border-b overflow-hidden h-7 flex items-center"
      style={{ backgroundColor: '#07080b', borderColor: 'var(--panel-border)' }}
      role="marquee"
      aria-label="Market overview ticker"
    >
      <div
        className="flex-none px-3 h-full flex items-center gap-1.5 border-r"
        style={{ borderColor: 'var(--panel-border)' }}
      >
        <span className="text-[9px] tracking-[0.14em] uppercase" style={{ color: 'var(--brand)' }}>
          B3
        </span>
        <span className="text-[9px] tracking-wider uppercase" style={{ color: 'var(--faint)' }}>
          overview
        </span>
      </div>

      <div className="flex-1 overflow-hidden relative">
        <div
          className="flex absolute top-0 left-0 h-7 items-center"
          style={{ transform: `translateX(-${tickerOffset}px)`, whiteSpace: 'nowrap', transition: 'none' }}
        >
          {[...tickerItems, ...tickerItems, ...tickerItems].map((item, i) => (
            <div
              key={i}
              className="flex items-center gap-2 px-5 border-r"
              style={{ borderColor: 'rgba(255,255,255,0.03)' }}
            >
              <span className="text-[11px] tracking-wider" style={{ color: 'var(--secondary-foreground)' }}>
                {item.symbol}
              </span>
              <span
                className="text-[11px] font-data"
                style={{ color: 'var(--foreground)' }}
              >
                {item.price.toFixed(2)}
              </span>
              <span
                className="text-[10px] flex items-center gap-0.5 font-data"
                style={{ color: item.change >= 0 ? 'var(--up)' : 'var(--down)' }}
              >
                {item.change >= 0
                  ? <ChevronUp className="w-2.5 h-2.5" aria-hidden="true" />
                  : <ChevronDown className="w-2.5 h-2.5" aria-hidden="true" />
                }
                {item.pct > 0 ? '+' : ''}{item.pct.toFixed(2)}%
              </span>
            </div>
          ))}
        </div>
      </div>

      <div
        className="flex-none px-3 border-l h-full flex items-center gap-2"
        style={{ borderColor: 'var(--panel-border)' }}
      >
        <time
          className="text-[10px] font-data"
          style={{ color: 'var(--muted-foreground)' }}
          dateTime={currentTime.toISOString()}
        >
          {currentTime.toLocaleDateString('en-GB')} · {currentTime.toLocaleTimeString('en-GB')}
        </time>
      </div>
    </div>
  );
}
