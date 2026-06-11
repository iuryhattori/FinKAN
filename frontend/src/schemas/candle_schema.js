// Mapper do DTO de candle da API para o modelo usado pela UI.
// Mantém o frontend desacoplado: se o contrato da API mudar, só este arquivo muda.

function requireNumber(value, field) {
  if (typeof value !== 'number' || Number.isNaN(value)) {
    throw new Error(`Invalid candle: field "${field}" is missing or not a number`);
  }
  return value;
}

/**
 * @param {object} dto payload de /api/v1/candles/* ou do campo "candle" do stream
 * @returns {{symbol: string, date: Date|null, open: number, high: number, low: number, close: number, volume: number}}
 */
export function parseCandle(dto) {
  if (!dto || typeof dto !== 'object') {
    throw new Error('Invalid candle: empty payload');
  }
  return {
    symbol: typeof dto.symbol === 'string' ? dto.symbol : '',
    date: typeof dto.date === 'number' ? new Date(dto.date * 1000) : null,
    open: requireNumber(dto.open, 'open'),
    high: requireNumber(dto.high, 'high'),
    low: requireNumber(dto.low, 'low'),
    close: requireNumber(dto.close, 'close'),
    volume: typeof dto.volume === 'number' ? dto.volume : 0,
  };
}
