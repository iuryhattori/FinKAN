import { useCallback, useEffect, useRef, useState } from 'react';
import {
  getCandleHistory,
  getLatestPrediction,
  subscribeMarketStream,
} from '../services/stockService';

const MAX_CANDLES = 200;
const MAX_HISTORY = 50;

function sameCandle(a, b) {
  if (!a || !b) return false;
  if (a.date && b.date) return a.date.getTime() === b.date.getTime();
  return a.open === b.open && a.high === b.high && a.low === b.low && a.close === b.close;
}

function samePrediction(a, b) {
  if (!a || !b) return false;
  return a.open === b.open && a.high === b.high && a.low === b.low && a.close === b.close;
}

/**
 * Estado de mercado em tempo real, alimentado exclusivamente pela API HTTP:
 * carga inicial via REST e atualizações contínuas via SSE.
 *
 * status: 'loading' | 'live' | 'reconnecting' | 'error'
 */
export function useMarketData({ historyLimit = 100 } = {}) {
  const [candles, setCandles] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [predictionHistory, setPredictionHistory] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  // Última predição vista pelo stream, para parear "predito vs. realizado"
  // sem sofrer com closures desatualizadas.
  const lastPredictionRef = useRef(null);

  const retry = useCallback(() => {
    setStatus('loading');
    setError(null);
    setRefreshKey((key) => key + 1);
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function bootstrap() {
      try {
        const [history, latestPrediction] = await Promise.all([
          getCandleHistory(historyLimit),
          getLatestPrediction(),
        ]);
        if (cancelled) return;
        setCandles(history);
        if (latestPrediction) {
          setPrediction(latestPrediction);
          lastPredictionRef.current = latestPrediction;
        }
        setStatus('live');
      } catch (err) {
        if (cancelled) return;
        setError(err);
        setStatus('error');
      }
    }

    function handleStreamData({ candle, prediction: newPrediction }) {
      setStatus('live');
      setError(null);

      setCandles((prev) => {
        if (sameCandle(prev.at(-1), candle)) return prev;
        return [...prev, candle].slice(-MAX_CANDLES);
      });

      if (newPrediction) {
        const previous = lastPredictionRef.current;
        // Predição nova: a anterior "venceu" — registra predito vs. realizado.
        if (previous && !samePrediction(previous, newPrediction)) {
          setPredictionHistory((prev) =>
            [
              ...prev,
              {
                timestamp: (candle.date ?? new Date()).toISOString(),
                predictedClose: previous.close,
                actualClose: candle.close,
                error: previous.close - candle.close,
              },
            ].slice(-MAX_HISTORY),
          );
        }
        lastPredictionRef.current = newPrediction;
        setPrediction(newPrediction);
      }
    }

    bootstrap();
    const unsubscribe = subscribeMarketStream({
      onData: handleStreamData,
      onError: () => {
        // O EventSource reconecta sozinho; só sinaliza o estado na UI.
        setStatus((prev) => (prev === 'live' ? 'reconnecting' : prev));
      },
    });

    return () => {
      cancelled = true;
      unsubscribe();
    };
  }, [historyLimit, refreshKey]);

  return { candles, prediction, predictionHistory, status, error, retry };
}
