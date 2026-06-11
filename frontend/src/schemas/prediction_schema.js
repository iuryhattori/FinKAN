// Mapper do DTO de predição da API para o modelo usado pela UI.
// O modelo prevê apenas OHLC (sem volume).

function requireNumber(value, field) {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    throw new Error(`Invalid prediction: field "${field}" is missing or not a number`);
  }
  return value;
}

/**
 * @param {object} dto payload de /api/v1/predictions/latest ou do campo "pred" do stream
 * @returns {{symbol: string, open: number, high: number, low: number, close: number}}
 */
export function parsePrediction(dto) {
  if (!dto || typeof dto !== 'object') {
    throw new Error('Invalid prediction: empty payload');
  }
  return {
    symbol: typeof dto.symbol === 'string' ? dto.symbol : '',
    open: requireNumber(dto.open, 'open'),
    high: requireNumber(dto.high, 'high'),
    low: requireNumber(dto.low, 'low'),
    close: requireNumber(dto.close, 'close'),
  };
}
