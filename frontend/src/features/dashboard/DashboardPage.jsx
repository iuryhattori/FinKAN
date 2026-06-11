import { useState, useEffect, useMemo } from 'react';
import { Activity, AlertTriangle, RefreshCw, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { TickerStrip } from './components/TickerStrip';
import { Header } from './components/Header';
import { MarketOverview } from './components/MarketOverview';
import { PredictionCard } from './components/PredictionCard';
import { PredictionChart } from './components/PredictionChart';
import { VolumeChart } from './components/VolumeChart';
import { PredictionHistoryTable } from './components/PredictionHistoryTable';
import { useMarketData } from '../../hooks/connection_hook';
import { buildPriceChartData, buildVolumeChartData } from './selectors';

// O modelo prevê apenas OHLC; volume não tem projeção.
const predictionFields = [
  { label: 'Abertura', key: 'open' },
  { label: 'Fechamento', key: 'close' },
  { label: 'Máxima', key: 'high' },
  { label: 'Mínima', key: 'low' },
];

/** Resumo em linguagem natural da projeção de fechamento. */
function TrendSummary({ current, prediction }) {
  const delta = prediction.close - current.close;
  const pct = (delta / current.close) * 100;
  const isFlat = Math.abs(pct) < 0.05;
  const isUp = delta >= 0;
  const tone = isFlat ? 'var(--muted-foreground)' : isUp ? 'var(--up)' : 'var(--down)';
  const Icon = isFlat ? Minus : isUp ? TrendingUp : TrendingDown;
  const phrase = isFlat
    ? 'estabilidade no fechamento da próxima hora'
    : `${isUp ? 'alta' : 'queda'} de ${Math.abs(pct).toFixed(2)}% no fechamento da próxima hora`;

  return (
    <p className="flex items-center gap-2 text-xs" style={{ color: 'var(--secondary-foreground)' }}>
      <Icon className="w-3.5 h-3.5 flex-none" style={{ color: tone }} aria-hidden="true" />
      <span>
        O modelo projeta{' '}
        <span style={{ color: tone, fontWeight: 600 }}>{phrase}</span>
        {' '}— de R$ {current.close.toFixed(2)} para{' '}
        <span className="font-data" style={{ color: 'var(--foreground)' }}>
          R$ {prediction.close.toFixed(2)}
        </span>.
      </span>
    </p>
  );
}

function SectionHeading({ title, children }) {
  return (
    <div className="flex items-center gap-3 mb-1">
      <h2 className="section-label">{title}</h2>
      <div className="h-px flex-1 max-w-24" style={{ backgroundColor: 'var(--border)' }} />
      {children}
    </div>
  );
}

function ErrorBanner({ error, onRetry }) {
  return (
    <div
      className="panel p-4 flex items-center justify-between"
      style={{ borderColor: 'rgba(229,73,95,0.3)' }}
      role="alert"
    >
      <div className="flex items-center gap-3">
        <AlertTriangle className="w-4 h-4" style={{ color: 'var(--down)' }} aria-hidden="true" />
        <div>
          <p className="text-xs" style={{ color: 'var(--foreground)' }}>
            Não conseguimos falar com os servidores agora.
          </p>
          <p className="text-[11px]" style={{ color: 'var(--muted-foreground)' }}>
            {error?.message ?? 'Erro desconhecido'} — verifique se a API FinKAN está no ar e tente de novo.
          </p>
        </div>
      </div>
      <button
        onClick={onRetry}
        className="flex items-center gap-1.5 px-3 py-1.5 rounded border text-[11px] uppercase tracking-widest transition-colors hover:bg-[#1a1e27]"
        style={{ color: 'var(--foreground)', borderColor: 'var(--border-strong)' }}
      >
        <RefreshCw className="w-3 h-3" aria-hidden="true" />
        Tentar de novo
      </button>
    </div>
  );
}

function WaitingPanel({ message }) {
  return (
    <div className="panel p-8 text-center">
      <Activity
        className="w-5 h-5 mx-auto mb-3 animate-pulse"
        style={{ color: 'var(--brand)' }}
        aria-hidden="true"
      />
      <p className="text-xs" style={{ color: 'var(--muted-foreground)' }}>
        {message}
      </p>
    </div>
  );
}

export function DashboardPage() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const { candles, prediction, predictionHistory, status, error, retry } = useMarketData();

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const currentData = candles.at(-1) ?? null;
  const priceChartData = useMemo(
    () => buildPriceChartData(candles, prediction),
    [candles, prediction],
  );
  const volumeChartData = useMemo(() => buildVolumeChartData(candles), [candles]);

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ backgroundColor: 'var(--background)', color: 'var(--foreground)' }}
    >
      <TickerStrip currentTime={currentTime} />
      <Header currentTime={currentTime} connectionStatus={status} />

      <main className="max-w-[1600px] w-full mx-auto px-6 py-5 space-y-5 flex-1">
        {status === 'error' && <ErrorBanner error={error} onRetry={retry} />}

        {status === 'loading' && (
          <WaitingPanel message="Conectando aos servidores FinKAN…" />
        )}

        {status !== 'loading' && status !== 'error' && !currentData && (
          <WaitingPanel message="Conexão estabelecida. Aguardando os primeiros candles do MetaTrader 5 — isso leva alguns segundos." />
        )}

        {currentData && (
          <>
            <MarketOverview currentData={currentData} />

            <section aria-label="Projeções para a próxima hora">
              <div className="mb-3 space-y-1.5">
                <SectionHeading title="Projeção · Próxima hora" />
                {prediction && <TrendSummary current={currentData} prediction={prediction} />}
              </div>

              {prediction ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5">
                  {predictionFields.map(({ label, key }) => (
                    <PredictionCard
                      key={key}
                      label={label}
                      current={currentData[key]}
                      predicted={prediction[key]}
                    />
                  ))}
                </div>
              ) : (
                <WaitingPanel message="O modelo está reunindo dados suficientes para a primeira projeção…" />
              )}
            </section>

            <section
              className="grid grid-cols-1 lg:grid-cols-5 gap-4"
              aria-label="Gráficos de mercado"
            >
              <div className="lg:col-span-3">
                <PredictionChart data={priceChartData} />
              </div>
              <div className="lg:col-span-2">
                <VolumeChart data={volumeChartData} />
              </div>
            </section>

            <section aria-label="Precisão das projeções">
              {predictionHistory.length > 0 ? (
                <PredictionHistoryTable history={predictionHistory} />
              ) : (
                <WaitingPanel message="Conforme novas projeções forem confrontadas com os preços realizados, o histórico de precisão do modelo aparece aqui." />
              )}
            </section>
          </>
        )}
      </main>

      <footer
        className="border-t px-6 py-3"
        style={{ backgroundColor: '#0d0f15', borderColor: 'var(--panel-border)' }}
      >
        <div
          className="max-w-[1600px] mx-auto flex items-center justify-between text-[10px]"
          style={{ color: 'var(--faint)' }}
        >
          <span>
            As projeções são geradas por um modelo estatístico e têm caráter exclusivamente
            informativo — não constituem recomendação de investimento.
          </span>
          <span className="font-data">FinKAN · PETR4 · horizonte 1h</span>
        </div>
      </footer>
    </div>
  );
}
