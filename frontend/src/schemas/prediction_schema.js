// Mapper do DTO de predição da API para o modelo usado pela UI.
// O modelo prevê apenas OHLC (sem volume).

function requireNumber(value, field) {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    throw new Error(`Predição inválida: campo "${field}" ausente ou não numérico`);
  }
  return value;
}

/**
 * @param {object} dto payload de /api/v1/predictions/latest ou do campo "pred" do stream
 * @returns {{symbol: string, open: number, high: number, low: number, close: number}}
 */
export function parsePrediction(dto) {
  if (!dto || typeof dto !== 'object') {
    throw new Error('Predição inválida: payload vazio');
  }
  return {
    symbol: typeof dto.symbol === 'string' ? dto.symbol : '',
    open: requireNumber(dto.open, 'open'),
    high: requireNumber(dto.high, 'high'),
    low: requireNumber(dto.low, 'low'),
    close: requireNumber(dto.close, 'close'),
  };
}
