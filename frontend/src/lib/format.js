// en-GB mantém formato 24h e dd/MM, coerente com o pregão da B3.
const LOCALE = 'en-GB';

// O MT5 grava o timestamp do candle como relógio de parede do pregão
// codificado em epoch ("falso UTC"). Formatar com timeZone: 'UTC' exibe
// esse relógio como está, sem o navegador deslocar para o fuso local.
const MT5_WALL_CLOCK = { timeZone: 'UTC' };

// Rótulo curto de horário para ticks de eixo (recebe timestamp em ms).
export function formatTickTime(value) {
  if (typeof value !== 'number') return value;
  return new Date(value).toLocaleTimeString(LOCALE, {
    hour: '2-digit',
    minute: '2-digit',
    ...MT5_WALL_CLOCK,
  });
}

// Data e hora completas para tooltips (recebe timestamp em ms).
export function formatFullTime(value) {
  if (typeof value !== 'number') return value;
  const d = new Date(value);
  const date = d.toLocaleDateString(LOCALE, { day: '2-digit', month: '2-digit', ...MT5_WALL_CLOCK });
  const time = d.toLocaleTimeString(LOCALE, { hour: '2-digit', minute: '2-digit', ...MT5_WALL_CLOCK });
  return `${date} · ${time}`;
}

// Formata volume de negociação com sufixo adaptativo (K/M/B).
// O tick volume real da B3 fica na casa de milhares; o formato fixo em
// milhões exibiria "0.0M" para dados reais.
export function formatVolume(value) {
  if (value == null || Number.isNaN(value)) return '—';
  const abs = Math.abs(value);
  if (abs >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
  if (abs >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
  return String(Math.round(value));
}
