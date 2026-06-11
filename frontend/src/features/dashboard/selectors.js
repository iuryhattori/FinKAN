// Transforma o modelo de mercado (candles/predição) no formato que os
// gráficos do dashboard consomem. Lógica de apresentação, não de negócio.
//
// O eixo X usa o timestamp (ms) como valor: é único por candle, então o
// hover e as linhas de referência nunca se confundem com horários repetidos
// de dias diferentes. A formatação para HH:MM acontece só na exibição.

const CANDLE_INTERVAL_MS = 15 * 60 * 1000;

function timeValue(candle, index) {
  return candle.date ? candle.date.getTime() : index;
}

export function buildPriceChartData(candles, prediction) {
  const data = candles.map((candle, index) => ({
    time: timeValue(candle, index),
    open: candle.open,
    close: candle.close,
  }));

  if (prediction && candles.length > 0) {
    const last = candles.at(-1);
    data.push({
      time: timeValue(last, candles.length - 1) + CANDLE_INTERVAL_MS,
      isPrediction: true,
      open: last.open,
      close: last.close,
      predictedOpen: prediction.open,
      predictedClose: prediction.close,
    });
  }
  return data;
}

export function buildVolumeChartData(candles) {
  // O modelo não prevê volume; o gráfico exibe apenas o volume realizado.
  return candles.map((candle, index) => ({
    time: timeValue(candle, index),
    volume: candle.volume,
  }));
}
