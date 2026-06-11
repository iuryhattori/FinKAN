// Camada de serviço da API FinKAN: única porta de entrada do frontend
// para o backend. Endpoints, parsing e tratamento de "sem dados" (404)
// ficam centralizados aqui.

import { API_BASE_URL, ApiError, getJson } from './httpClient';
import { parseCandle } from '../schemas/candle_schema';
import { parsePrediction } from '../schemas/prediction_schema';

/** Última vela coletada, ou null se o backend ainda não tem dados. */
export async function getLatestCandle(options) {
  try {
    const dto = await getJson('/api/v1/candles/latest', options);
    return parseCandle(dto);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  }
}

/** Histórico das últimas velas coletadas, do mais antigo ao mais recente. */
export async function getCandleHistory(limit = 100, options) {
  const dto = await getJson(`/api/v1/candles/history?limit=${limit}`, options);
  return (dto?.candles ?? []).map(parseCandle);
}

/** Última predição do modelo, ou null se ainda não há predição. */
export async function getLatestPrediction(options) {
  try {
    const dto = await getJson('/api/v1/predictions/latest', options);
    return parsePrediction(dto);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  }
}

/**
 * Assina o stream SSE de mercado (/api/v1/stream).
 * O EventSource reconecta automaticamente em caso de queda.
 *
 * @param {object} handlers
 * @param {(data: {candle: object, prediction: object|null}) => void} handlers.onData
 * @param {() => void} [handlers.onError] chamado a cada falha de conexão
 * @param {() => void} [handlers.onOpen] chamado quando a conexão estabelece
 * @returns {() => void} função para encerrar a assinatura
 */
export function subscribeMarketStream({ onData, onError, onOpen }) {
  const source = new EventSource(`${API_BASE_URL}/api/v1/stream`);

  source.onopen = () => onOpen?.();

  source.onmessage = (event) => {
    let payload;
    try {
      payload = JSON.parse(event.data);
    } catch (err) {
      console.warn('[stream] mensagem descartada: JSON inválido', err);
      return;
    }

    try {
      onData({
        candle: parseCandle(payload.candle),
        prediction: payload.pred ? parsePrediction(payload.pred) : null,
      });
    } catch (err) {
      console.warn('[stream] mensagem descartada: contrato inválido', err);
    }
  };

  source.onerror = () => onError?.();

  return () => source.close();
}
